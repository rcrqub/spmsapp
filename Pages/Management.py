import streamlit as st
import pandas as pd

st.set_page_config(page_title="SPMS",page_icon=':toilet:')
st.title("Bathroom and Product Management")

df = pd.read_csv('BathroomData.csv')

md = 'Here you can create new bathroom, or remove old ones. Additioanly, you can add and manage the products you have available.'
st.markdown(md)

IDS = df['bathroom_id'].unique()
DESC = df['bathroom_descrption'].unique()

st.subheader('Available Bathrooms')

edited_df = st.data_editor(df)