from typing import Type
import streamlit as st 
import pandas as pd

# Home Page Text and Setup
st.set_page_config(page_title="SPMS", page_icon=':toilet:')
st.title("Sanitary Product Management System")

# Introduction
st.header("Welcome to SPMS :wave:")
st.markdown(
    "The Sanitary Product Management System (SPMS) is designed by *Robert Craig*, *Daniel Quinn*, and *Adam Exley*. "
    "This system aims to streamline and enhance the management of sanitary products, with a focus on Feminine Hygiene Products."
)

# Importing Bathroom Data
df = pd.read_csv('BathroomData.csv')

# Product Usage Section
st.header('Product Usage')
# TODO: Add a plot or visualization for total product usage over time

# Stock Low Alerts Section
st.header('Stock Low Alerts')
stock_warning_thres = st.number_input("Set the Stock Warning Threshold:", step=1, placeholder="Enter a number...")

for _, row in df.iterrows():
    if row['stock_level'] <= stock_warning_thres:
        item_type = row['item_type'].replace("_", " ").capitalize()
        bathroom_id = row['bathroom_id']
        st.markdown(f":warning: {item_type} is low in Bathroom {bathroom_id}")

# TODO: Add more sections as needed