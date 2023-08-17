import plotly.express as px
import streamlit as st
import json
import pandas as pd

# Load data and configuration from the JSON files
with open('sl_graph_data.json', 'r') as data_file:
    data_config = json.load(data_file)

with open('sl_graph_hist_config.json', 'r') as hist_file:
    hist_config = json.load(hist_file)

# Convert data to DataFrame
df = pd.DataFrame(data_config["data"])

# Display histogram
st.title(hist_config["chart_title"])
fig = px.histogram(
    df, 
    x=hist_config["x_axis"]["column"],
    color=hist_config["group_by"],
    title=hist_config["chart_title"],
    labels={
        hist_config["x_axis"]["column"]: data_config["headers"][hist_config["x_axis"]["column"]],
        hist_config["group_by"]: data_config["headers"][hist_config["group_by"]]
    }
)
st.plotly_chart(fig, use_container_width=True)
