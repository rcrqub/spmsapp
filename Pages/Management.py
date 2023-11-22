import streamlit as st
import pandas as pd
from streamlit_float import *

st.set_page_config(page_title="SPMS",page_icon=':toilet:')
st.title("Bathroom and Product Management")

df = pd.read_csv('BathroomData.csv')

md = 'Here you can create new bathroom, or remove old ones. Additionaly, you can add and manage the products you have available.'
st.markdown(md)

IDS = df['bathroom_id'].unique()
DESC = df['bathroom_descrption'].unique()
PROD = df['item_type'].unique()

st.subheader('Available Bathrooms :toilet:')

float_init()
if "show" not in st.session_state:
    st.session_state.show = False

# Create Float Dialog container
dialog_container = float_dialog(st.session_state.show)

# Add contents of Dialog including button to close it
with dialog_container:
    add_input = st.text_input("Enter a Bathroom Description", key='add')
    if st.button("Send", key="send"):
        add(add_input)
        st.session_state.show = False
        st.experimental_rerun()

def add(text):
    df2['bathroom_id'] = len(IDS) + 1
    df2['bathroom_descrption'] = text
    df.append(df2)
    df.to_csv('BathroomData.csv')

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Bathroom ID**")
    for i in range(len(IDS)):
        st.write(f"{IDS[i]}")
    if st.button('Add Bathroom', key=add):
        st.session_state.show = True
        st.experimental_rerun()

with col2:
    st.markdown("**Description**")
    for i in range(len(IDS)):
        st.write(f"{DESC[i]}")

with col3:
    st.markdown("**Remove Bathroom**")
#    for i in range(len(IDS)):
#        st.button('❌', key=remove)