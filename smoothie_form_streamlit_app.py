# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customise Your Smoothie :cup_with_straw:")
st.write(
    f"""Choose your fruits in your custom smoothie!
    """
)

# Get the current credentials
cnx = st.connection("snowflake")
session = cnx.session()

# fruit_option = st.selectbox(
#    'What is your favourite fruit?',
#    ('Banana', 'Strawberry', 'Peach')
# )
# st.write('You selected:', fruit_option)

name_order = st.text_input('Name on the smoothie:')
st.write('Order for: ', name_order)

fruit_df = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=fruit_df, use_container_width=True)
ingredients_list = st.multiselect('Choose up to 5 ingredients:', fruit_df, max_selections=5)

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    ingredients_string = ''
    for f_chosen in ingredients_list:
        ingredients_string += f_chosen + " "
    #st.write(ingredients_string)

    
    # Build the query
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '""" +name_order+"""')"""
    #st.write(my_insert_stmt)

    # Write to DB to button trigger
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        if ingredients_string:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")
