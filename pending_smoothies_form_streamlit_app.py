# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col, when_matched

# Write directly to the app
st.title(":cup_with_straw: Pending Smoothie Orders :cup_with_straw:")
st.write(
    f"""Orders to fill!
    """
)

# Get the current credentials
cnx = st.connect("snowflake")
session = cnx.session()

orders_df = (
    session.table("smoothies.public.orders")
    .filter(col('ORDER_FILLED') == False)  # Filter where ORDER_FILLED is False
)

if orders_df.count() > 0:
    # st.dataframe(data=orders_df, use_container_width=True)
    editable_df = st.data_editor(orders_df)
    
    time_to_insert = st.button('Submit')
    if time_to_insert:
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)
        try:
            og_dataset.merge(edited_dataset
                , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
            )
            st.success('Order filled!', icon="👍")
        except:
            st.write('Error: Something went wrong submit again')
else:
    st.write('No pending orders')
