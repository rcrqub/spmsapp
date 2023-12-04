import streamlit as st
import pandas as pd

# Read the CSV data from a file
file_path = "ReportingDataMonth.csv"
df = pd.read_csv(file_path)

df_filtered = df.groupby(['bathroom_id', 'item_type']).tail(1)
bathroomData = df_filtered.drop(["year", "month", "day", "hour"], axis=1)



