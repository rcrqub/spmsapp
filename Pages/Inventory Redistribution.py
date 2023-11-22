import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(page_title="SPMS", page_icon="🚽")
st.title("Inventory Redistribution")

# Read data
df = pd.read_csv('BathroomData.csv')

# Product selection dropdown
selected_product = st.selectbox(
    'Which product would you like to redistribute?', 
    ("Heavy Pad", "Medium Pad", "Light Pad"),
    help="Select the product you want to redistribute."
)

# Display selected product
st.write('You selected:', selected_product)

# Format selection for DataFrame filtering
selected_product = selected_product.replace(" ", "_").lower()

# Filter DataFrame based on selected product
selected_df = df.loc[df['item_type'] == selected_product]

# Bathroom selection for redistribution
selected_bathrooms = st.multiselect(
    'Select the bathrooms for redistribution:', 
    selected_df['bathroom_id'].unique(),
    help="Choose the bathrooms you want to redistribute to."
)

# Calculate mean stock level
mean_stock_level = selected_df['stock_level'].mean()

# Display redistribution information for selected bathrooms
for _, row in selected_df[selected_df['bathroom_id'].isin(selected_bathrooms)].iterrows():
    stock_difference = int(mean_stock_level) - row['stock_level']
    bathroom_id = row['bathroom_id']

    if stock_difference < 0:
        st.warning(f"Remove {abs(stock_difference)} items from Bathroom {bathroom_id}")
    elif stock_difference > 0:
        st.success(f"Add {stock_difference} items to Bathroom {bathroom_id}")
    else:
        st.info(f"Bathroom {bathroom_id} has the optimal stock level")
