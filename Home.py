from typing import Type
import streamlit as st 
import pandas as pd

import pickle
from pathlib import Path
import streamlit_authenticator as stauth

# User Auth
names = ['Daniel Quinn', 'Adam Exley', 'Robert Craig']
usernames = ['dquinn','aexley','rcraig']

file_path = Path(__file__).parent / "hased_pw.pk1"
with file_path.open('rb') as file:
    hashed_passwords = pickle.load(file)

credentials = {
    "usernames":{
        usernames[0]:{
            "name":names[0],
            "password":hashed_passwords[0]
            },
        usernames[1]:{
            "name":names[1],
            "password":hashed_passwords[1]
            }, 
        usernames[2]:{
            "name":names[2],
            "password":hashed_passwords[2]
            }         
        }
    }

authenticator = stauth.Authenticate(credentials, "spms", "auth", cookie_expiry_days=30)

# Create a session state object
if "authentication_status" not in st.session_state:
    st.session_state.authentication_status = None


name, authentication_status, username = authenticator.login("Login", 'main')

# Handle authentication status
if authentication_status is False:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username and password')
elif authentication_status:
    # Set the authentication status in session state
    st.session_state.authentication_status = authentication_status

    # Introduction
    authenticator.logout("Logout", 'sidebar')

    st.header(f"Welcome, {name}, to SPMS :wave:")
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