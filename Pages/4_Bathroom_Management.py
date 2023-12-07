import streamlit as st
import pandas as pd
import streamlit as st 
import pickle
from pathlib import Path
import streamlit_authenticator as stauth

# User Auth
names = ['Daniel Quinn', 'Adam Exley', 'Robert Craig']
usernames = ['dquinn','aexley','rcraig']

file_path = Path(__file__).parent.parent / "hased_pw.pk1"
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

name, authentication_status, username = authenticator.login("Login to the SPMS", 'main')

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

    current_data = pd.read_csv('BathroomData.csv')

    st.header("Bathroom Management")
    IDS = current_data['bathroom_id'].unique()

    # Function to add a new bathroom
    def add_bathroom(text):
        new_bathroom = {'bathroom_id': len(IDS) + 1, 'bathroom_description': text}
        current_data.loc[len(current_data)] = new_bathroom
        current_data.to_csv('BathroomData.csv', index=False)

    # Function to remove a bathroom
    def remove_bathroom(bathroom_description):
        current_data.drop(current_data[current_data.bathroom_description == bathroom_description].index, inplace=True)
        current_data.to_csv('BathroomData.csv', index=False)

    # User interface for adding a bathroom

    with st.form("Add Bathroom"):
        desc = st.text_input("Please Enter a Description:")

        # Every form must have a submit button.
        submitted = st.form_submit_button("Confirm")
        if submitted:
            add_bathroom(desc)
            st.success(f"Bathroom '{desc}' added successfully.")

    with st.form("Remove Bathroom"):
        bathroom_to_remove = st.selectbox("Select Bathroom to Remove", current_data['bathroom_description'].unique())

        # Every form must have a submit button.
        submitted = st.form_submit_button("Confirm")
        if submitted:
            remove_bathroom(bathroom_to_remove)
            st.success(f"Bathroom '{bathroom_to_remove}' removed successfully.")


    st.subheader('Bathroom\'s Available')
    col1, col2= st.columns(2)

    with col1:
        st.markdown("*Bathroom ID*")
        for bathroom_id in current_data['bathroom_id'].unique():
            st.write(f"{bathroom_id}")

    with col2:
        st.markdown("*Description*")
        for description in current_data['bathroom_description'].unique():
            st.write(f"{description}")
