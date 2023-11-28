import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="SPMS",page_icon=':toilet:')
st.title("Live Reporting")

# Read the CSV data
df = pd.read_csv('ReportingData.csv')

# Convert columns to appropriate types
df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']].astype(str).agg('-'.join, axis=1), format='%Y-%m-%d-%H')
df['stock_level'] = df['stock_level'].astype(int)

# Create a new column combining bathroom_id and item_type
df['group'] = df['bathroom_id'].astype(str) + ' ' + df['item_type']

view_option = st.radio("Select View", ["Bathroom ID - Item Type", "Item Type Only", "Total Quantity by Item Type"])

# Create a multiline chart using Altair based on the selected view option
if view_option == "Bathroom ID - Item Type":
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