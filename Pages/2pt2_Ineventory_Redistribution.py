import streamlit as st
import pandas as pd

# Read the CSV data from a file
file_path = "BathroomData.csv"
df = pd.read_csv(file_path)

# Page configuration
st.set_page_config(page_title="SPMS", page_icon="🚽")
st.title("Inventory Redistribution")

# Display the original DataFrame
st.subheader('Original Data')
st.write(df)

# Calculate the total quantity of each item_type
total_quantity_by_item_type = df.groupby('item_type')['stock_level'].sum().reset_index()

# Display the total quantity by item_type
st.subheader('Total Quantity by Item Type')
st.write(total_quantity_by_item_type)

# Calculate the average quantity per bathroom for each item_type
average_quantity_per_bathroom = total_quantity_by_item_type['stock_level'] / df['bathroom_id'].nunique()

# Create a new DataFrame for redistributed data
redistributed_df = pd.DataFrame()

# Redistribute the items evenly across bathrooms for each item_type
for _, row in total_quantity_by_item_type.iterrows():
    item_type = row['item_type']
    total_quantity = row['stock_level']
    average_quantity = average_quantity_per_bathroom[item_type]
    
    # Calculate the quantity to assign to each bathroom
    quantity_per_bathroom = total_quantity / df['bathroom_id'].nunique()
    
    # Create a DataFrame for the redistributed data
    redistributed_item_type_df = pd.DataFrame({
        'datetime': df['datetime'],
        'bathroom_id': df['bathroom_id'],
        'item_type': item_type,
        'stock_level': quantity_per_bathroom
    })
    
    # Append the redistributed data to the main redistributed DataFrame
    redistributed_df = pd.concat([redistributed_df, redistributed_item_type_df])

# Display the redistributed DataFrame
st.subheader('Redistributed Data')
st.write(redistributed_df)