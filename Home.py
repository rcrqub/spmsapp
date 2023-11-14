from typing import Type
import streamlit as st 
import pandas as pd

# Home Page Text and Setup
st.set_page_config(page_title="SPMS",page_icon=':toilet:')
st.title("Sanitary Product Management System")
md = 'Welcome :wave: to the Sanitary Product Management System (SPMS) designed by *Robert Craig*, *Daniel Quinn* and *Adam Exley*. This system aims to streamline and enhance the management of sanitary products focusing on Feminie Hygine Products.'
st.markdown(md)

# Importing Bathroom Data
df = pd.read_csv('BathroomData.csv')

st.subheader('Product Usage')
# MAYBE A GOOD IDEA TO ADD A TOTAL PRODUCT USAGE OVER TIME 

st.subheader('Stock Low Alerts')
stock_warning_thres = st.number_input("Please set the Stock Warning Threshold: ", step = 1, placeholder="Type a number...")
for _, row in df.iterrows():
    if row['stock_level'] <= stock_warning_thres:
        str = row['item_type'].replace("_"," ")
        str = str.capitalize()
        st.markdown(f" :warning: {str} is low in Bathroom {row['bathroom_id']}")