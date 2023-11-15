import streamlit as st
import pandas as pd

st.set_page_config(page_title="SPMS",page_icon="🚽")
st.title("Inventory Redistubution")

df = pd.read_csv('BathroomData.csv')

selection = st.selectbox(
    'Which Product would you like to Redistrubute?', 
    ("Heavy Pad","Medium Pad","Light Pad"),
    placeholder = "Select Product")

st.write('You selected:', selection) 

selection = selection.replace(" ", "_")
selection = selection.lower()

selected_df = df.loc[df['item_type'] == selection]
mean = selected_df.mean(axis=0, numeric_only = True)
for _, row in selected_df.iterrows():
    if int(mean['stock_level']) - row['stock_level'] < 0:
        st.write(f" :: Please Remove {row['stock_level']-int(mean['stock_level'])} Items from Bathroom {row['bathroom_id']}")
    else:
        st.write(f" Please Add {int(mean['stock_level']) - row['stock_level']} Items to Bathroom {row['bathroom_id']}")