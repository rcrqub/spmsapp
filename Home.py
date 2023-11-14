from typing import Type
import streamlit as st 
import pandas as pd

# Home Page Text and Setup
st.set_page_config(page_title="SPMS",page_icon=':toilet:')
st.title("Sanitary Product Management System")
md = 'Welcome :wave: to the Sanitary Product Management System designed by *Robert Craig*, *Daniel Quinn* and *Adam Exley* for the CSC4008: Digital Transformation module.'
st.markdown(md)

# Importing Bathroom Data
df = pd.read_csv('BathroomData.csv')
st.write(df)

st.subheader('Stock Low')
stock_warning_thres = st.number_input("Please set the Stock Warning Threshold: ", step = 1, placeholder="Type a number...")
for _, row in df.iterrows():
    if row['stock_level'] <= stock_warning_thres:
        st.write(f" ❗ {row['item_type']} is low in Bathroom {row['bathroom_id']}")