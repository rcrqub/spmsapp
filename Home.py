from typing import Type
import streamlit as st 
import pandas as pd
import altair as alt

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

    st.header(f"Welcome, {name}, to SPMS :wave:")
    st.markdown(
        "The Sanitary Product Management System (SPMS) is designed by *Robert Craig*, *Daniel Quinn*, and *Adam Exley*. "
        "This system aims to streamline and enhance the management of sanitary products, with a focus on Feminine Hygiene Products."
    )

    # Importing All Bathroom Data
    df = pd.read_csv('ReportingData.csv')
    pd.to_datetime(df[['year','month','day','hour']])
    current_date = df[['year','month','day','hour']].max()
    current_data = df.loc[(df['year'] == current_date['year'])
                     & (df['month'] == current_date['month'])
                     & (df['day'] == current_date['day'])
                     & (df['hour'] == current_date['hour'])]


    # Product Usage Section
    st.subheader('Product Usage')

    # Convert columns to appropriate types
    df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']].astype(str).agg('-'.join, axis=1), format='%Y-%m-%d-%H')
    df['stock_level'] = df['stock_level'].astype(int)

    # Create a new column combining bathroom_id and item_type
    df['group'] = df['bathroom_id'].astype(str) + ' ' + df['item_type']

    total_quantity_by_bathroom = df.groupby(['datetime', 'bathroom_id']).agg({'stock_level': 'sum'}).reset_index()
    chart1 = alt.Chart(total_quantity_by_bathroom).mark_line().encode(
        x='datetime:T',
        y='stock_level:Q',
        color=alt.Color('bathroom_id:N', legend=alt.Legend(title='Bathroom ID')),
        tooltip=['datetime:T', 'stock_level:Q', 'bathroom_id:N']
    ).properties(
        width=800,
        height=400,
        title='Bathroom ID'
    )

    chart2 = alt.Chart(df.groupby(['datetime', 'item_type']).agg({'stock_level': 'sum'}).reset_index()).mark_line().encode(
        x='datetime:T',
        y='stock_level:Q',
        color=alt.Color('item_type:N', legend=alt.Legend(title='Item Type')),
        tooltip=['datetime:T', 'stock_level:Q', 'item_type:N']
    ).properties(
        width=800,
        height=400,
        title='Item Type'
    )

    col1, col2 = st.columns(2)

    with col1:
        st.altair_chart(chart1, use_container_width=True)
    with col2:
        st.altair_chart(chart2, use_container_width=True)

    # Stock Low Alerts Section
    st.header('Stock Low Alerts')
    stock_warning_thres = st.number_input("Set the Stock Warning Threshold:", step=1, placeholder="Enter a number...")

    for _, row in current_data.iterrows():
        if row['stock_level'] <= stock_warning_thres:
            item_type = row['item_type'].replace("_", " ").capitalize()
            bathroom_id = row['bathroom_id']
            st.markdown(f":warning: {item_type} is low in Bathroom {bathroom_id}")
