import streamlit as st
import pandas as pd
from streamlit_float import float_dialog

st.set_page_config(page_title="SPMS", page_icon=':toilet:')
st.title("Bathroom Management")

df = pd.read_csv('ReportingData.csv')
pd.to_datetime(df[['year','month','day','hour']])
current_date = df[['year','month','day','hour']].max()
current_data = df.loc[(df['year'] == current_date['year'])
                     & (df['month'] == current_date['month'])
                     & (df['day'] == current_date['day'])
                     & (df['hour'] == current_date['hour'])]

md = 'Here you can create new bathrooms or remove old ones. Additionally, you can manually manage the products you have available.'
st.markdown(md)

IDS = current_data['bathroom_id'].unique()
DESC = current_data['bathroom_description'].unique()

def add_bathroom(text):
    new_bathroom = {'bathroom_id': len(IDS) + 1, 'bathroom_description': text}
    current_data.loc[len(current_data)] = new_bathroom
    current_data.to_csv('BathroomData.csv', index=False)

def remove_bathroom(bathroom_id):
    current_data.drop(current_data[current_data.bathroom_id == bathroom_id].index, inplace=True)
    current_data.to_csv('BathroomData.csv', index=False)

st.subheader('Available Bathrooms :toilet:')

if "show" not in st.session_state:
    st.session_state.show = False

# Create Float Dialog container
dialog_container = float_dialog(st.session_state.show)

# Add contents of Dialog including button to close it
with dialog_container:
    add_input = st.text_input("Enter a Bathroom Description", key='add')
    if st.button("Accept", key="send"):
        if add_input.strip() != "":
            add_bathroom(add_input)
            st.session_state.show = False
            st.experimental_rerun()

# Refresh IDS and DESC after adding a new bathroom
IDS = current_data['bathroom_id'].unique()
DESC = current_data['bathroom_description'].unique()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("*Bathroom ID*")
    for bathroom_id in IDS:
        st.write(f"{bathroom_id}")
    if st.button('🟢 Add Bathroom'):
        st.session_state.show = True

with col2:
    st.markdown("*Description*")
    for description in DESC:
        st.write(f"{description}")

with col3:
    st.markdown("*Remove Bathroom*")
    for bathroom_id in IDS:
        if st.button(f'❌ Remove', key=bathroom_id):
            remove_bathroom(bathroom_id)
            st.experimental_rerun()
