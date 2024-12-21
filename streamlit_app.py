# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests


# Write directly to the app
st.title("Customise Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruit you want in your custom smoothie!
    """
)

title = st.text_input("Name on smoothie:")
st.write("The name on your smoothie will be: ", title)

cnx = st.connection("snowflake")
session = cnx.session()
my_data_frame = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe (data = my_data_frame, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to five ingredients:'
    , my_data_frame
    , max_selections = 5
                                 )
if ingredients_list:
    ingredients_string=''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_cosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" = fruit_chosen)
        sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, NAME_ON_ORDER)
            values ('""" + ingredients_string + """', '""" + title + """')"""

    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order!')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
    
        st.success('Your Smoothie is ordered!', icon="✅")



                                            
