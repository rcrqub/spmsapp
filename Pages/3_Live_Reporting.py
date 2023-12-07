import streamlit as st
import pandas as pd
import altair as alt
from streamlit_float import float_dialog
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

    st.header("Live Reporting")

    # Read the CSV data
    df = pd.read_csv('ReportingDataMonth.csv')

    # Convert "year," "month," and "day" to datetime
    df['date'] = pd.to_datetime(df[['year', 'month', 'day']])

    # Extract the date of the last full day
    last_full_day = df['date'].iloc[-1].date()

    # Filter the DataFrame for the last full day
    df_filtered = df[df['date'].dt.date == last_full_day]

    # Drop the additional 'date' column if needed
    dfDay = df_filtered.drop('date', axis=1)

    # Convert columns to appropriate types
    dfDay['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']].astype(str).agg('-'.join, axis=1), format='%Y-%m-%d-%H')
    dfDay['stock_level'] = dfDay['stock_level'].astype(int)

    # Create a new column combining bathroom_id and item_type
    dfDay['group'] = dfDay['bathroom_id'].astype(str) + ' ' + dfDay['item_type']

    view_option = st.radio("Select View", ["Bathroom ID - Item Type", "Item Type Only", "Total Quantity by Item Type"])

    # Create a multiline chart using Altair based on the selected view option
    if view_option == "Bathroom ID - Item Type":
        chart = alt.Chart(dfDay).mark_line().encode(
            x='datetime:T',
            y='stock_level:Q',
            color=alt.Color('group:N', legend=alt.Legend(title='Bathroom ID - Item Type')),
            tooltip=['datetime:T', 'stock_level:Q', 'group:N']
        ).properties(
            width=800,
            height=400,
            title='Stock Level Over Time Grouped by Bathroom ID and Item Type'
        )
    elif view_option == "Item Type Only":
        chart = alt.Chart(dfDay.groupby(['datetime', 'item_type']).agg({'stock_level': 'sum'}).reset_index()).mark_line().encode(
            x='datetime:T',
            y='stock_level:Q',
            color=alt.Color('item_type:N', legend=alt.Legend(title='Item Type')),
            tooltip=['datetime:T', 'stock_level:Q', 'item_type:N']
        ).properties(
            width=800,
            height=400,
            title='Stock Level Over Time by Item Type'
        )
    else:
        total_quantity_by_bathroom = dfDay.groupby(['datetime', 'bathroom_id']).agg({'stock_level': 'sum'}).reset_index()
        chart = alt.Chart(total_quantity_by_bathroom).mark_line().encode(
            x='datetime:T',
            y='stock_level:Q',
            color=alt.Color('bathroom_id:N', legend=alt.Legend(title='Bathroom ID')),
            tooltip=['datetime:T', 'stock_level:Q', 'bathroom_id:N']
        ).properties(
            width=800,
            height=400,
            title='Total Quantity Over Time by Bathroom ID'
        )

    # Display the chart
    st.altair_chart(chart, use_container_width=True)



    # Convert columns to appropriate types
    df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']].astype(str).agg('-'.join, axis=1), format='%Y-%m-%d-%H')
    df['stock_level'] = df['stock_level'].astype(int)

    # Create a new column combining bathroom_id and item_type
    df['group'] = df['bathroom_id'].astype(str) + ' ' + df['item_type']

    view_option = st.radio("Select View", ["Bathroom ID : Item Type", "Item Type Only", "Total Quantity by Item Type"])

    # Create a multiline chart using Altair based on the selected view option
    if view_option == "Bathroom ID : Item Type":
        chart = alt.Chart(df).mark_line().encode(
            x='datetime:T',
            y='stock_level:Q',
            color=alt.Color('group:N', legend=alt.Legend(title='Bathroom ID - Item Type')),
            tooltip=['datetime:T', 'stock_level:Q', 'group:N']
        ).properties(
            width=800,
            height=400,
            title='Stock Level Over Time Grouped by Bathroom ID and Item Type'
        )
    elif view_option == "Item Type Only":
        chart = alt.Chart(df.groupby(['datetime', 'item_type']).agg({'stock_level': 'sum'}).reset_index()).mark_line().encode(
            x='datetime:T',
            y='stock_level:Q',
            color=alt.Color('item_type:N', legend=alt.Legend(title='Item Type')),
            tooltip=['datetime:T', 'stock_level:Q', 'item_type:N']
        ).properties(
            width=800,
            height=400,
            title='Stock Level Over Time by Item Type'
        )
    else:
        total_quantity_by_bathroom = df.groupby(['datetime', 'bathroom_id']).agg({'stock_level': 'sum'}).reset_index()
        chart = alt.Chart(total_quantity_by_bathroom).mark_line().encode(
            x='datetime:T',
            y='stock_level:Q',
            color=alt.Color('bathroom_id:N', legend=alt.Legend(title='Bathroom ID')),
            tooltip=['datetime:T', 'stock_level:Q', 'bathroom_id:N']
        ).properties(
            width=800,
            height=400,
            title='Total Quantity Over Time by Bathroom ID'
        )

    # Display the chart
    st.altair_chart(chart, use_container_width=True)