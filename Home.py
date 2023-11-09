import streamlit as st 
import pandas as pd

# Home Page Text and Setup
st.set_page_config(page_title="SPMS",page_icon="🚽",)
st.title("Sanitary Product Management System")
md = 'Welcome :wave: to the Sanitary Product Management System designed by *Robert Craig*, *Daniel Quinn* and *Adam Exley* for the CSC4008: Digital Transformation module.'
st.markdown(md)

# Importing Bathroom Data
df = pd.read_csv('BathroomData.csv')
st.write(df)

st.markdown('**Stock Low**')
# Stock Warnings (Toast Notification)
stock_warning_thres = 3
for _, row in df.iterrows():
    if row['stock_level'] <= stock_warning_thres:
        st.error(f"{row['item_type']} is low in Bathroom {row['bathroom_id']}", icon="❗")
