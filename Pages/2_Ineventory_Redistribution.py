import streamlit as st
import pandas as pd
import numpy as np

def redistribute_items(df):

    # Group by bathroom_id and item_type, and calculate the total stock_level for each group
    grouped_df = df.groupby(['bathroom_id', 'item_type'])['stock_level'].sum().reset_index()
    

    # Calculate the average stock_level for each item_type
    avg_stock_per_item = grouped_df.groupby('item_type')['stock_level'].mean()

    # Function to redistribute stock evenly across bathrooms for a given item_type
    def redistribute_item_type(group):
        item_type = group['item_type'].iloc[0]
        group['stock_level'] = np.floor(avg_stock_per_item[item_type])
        return group

    # Apply the redistribution function to each group (item_type)
    redistributed_df = grouped_df.groupby('item_type').apply(redistribute_item_type)

    # Reset index to avoid MultiIndex
    redistributed_df = redistributed_df.reset_index(drop=True)

    # Sort the redistributed data by bathroom_id and item_type
    redistributed_df = redistributed_df.sort_values(by=['bathroom_id', 'item_type'])

    # Convert stock_level column to integers
    redistributed_df['stock_level'] = redistributed_df['stock_level'].astype(int)

    return redistributed_df


def redistribution_summary(original_df, redistributed_df):
    summary = []
    
    for index, row in original_df.iterrows():
        bathroom_id = row['bathroom_id']
        item_type = row['item_type']
        original_stock = row['stock_level']
        redistributed_stock = redistributed_df.loc[
            (redistributed_df['bathroom_id'] == bathroom_id) & (redistributed_df['item_type'] == item_type),
            'stock_level'
        ].iloc[0]

        difference = redistributed_stock - original_stock
        difference_str = f"&#43;{int(difference)}" if difference > 0 else str(int(difference)) #&#43;='+' in ASCII

        summary.append({
            'Bathroom ID': bathroom_id,
            'Item Type': item_type,
            'Original Stock': original_stock,
            'Redistributed Stock': redistributed_stock,
            'Difference': difference_str
        })
    
    summary_df = pd.DataFrame(summary)

    # Sort the summary by item_type and then by bathroom_id
    summary_df = summary_df.sort_values(by=['Item Type', 'Bathroom ID'])
    display_markdown_table(summary_df, "Redistribution Summary")

    # Group by bathroom_id and item_type, and calculate the total stock_level for each group
    original_spare_df = original_df.groupby(['bathroom_id', 'item_type'])['stock_level'].sum().reset_index()
    redistributed_spare_df = redistributed_df.groupby(['bathroom_id', 'item_type'])['stock_level'].sum().reset_index()

    # Calculate the average stock_level for each item_type
    total_original_item = original_spare_df.groupby('item_type')['stock_level'].sum()
    total_redistributed_item = redistributed_spare_df.groupby('item_type')['stock_level'].sum()

    spare_items = total_original_item - total_redistributed_item

    # Spare stock  Alerts Section
    st.subheader('Spare Stock')
    for item_type, level in spare_items.items():
        if level != 0:
            if level == 1:
                st.markdown(f' :warning: There is {int(level)} spare {item_type.replace("_", " ")}')
            else:
                st.markdown(f' :warning: There are {int(level)} spare {item_type.replace("_", " ")}s')
def display_markdown_table(df, title):
    st.subheader(title)
    st.markdown(df.to_markdown(index=False), unsafe_allow_html=True)

# Read the CSV data from a file
file_path = "ReportingDataMonth.csv"
df = pd.read_csv(file_path)

df_filtered = df.groupby(['bathroom_id', 'item_type']).tail(1)
bathroomData = df_filtered.drop(["year", "month", "day", "hour"], axis=1)
dist = redistribute_items(bathroomData)

# Page configuration
st.set_page_config(page_title="SPMS", page_icon="🚽")
st.title("Inventory Redistribution")
redistribution_summary(bathroomData, dist)
