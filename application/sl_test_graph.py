import openai

import plotly.express as px
import streamlit as st
import pandas as pd
import helpers

def generate_plot():
    # Load data and configuration from the JSON files
    data_config = helpers.load_json("./application/sl_graph_data.json")
    bar_config = helpers.load_json("./application/sl_graph_config/sl_graph_bar_config.json")  # Keeping the file name the same as provided

    # Convert data to DataFrame
    df = pd.DataFrame(data_config["data"])

    # Display bar chart
    st.title(bar_config["chart_title"])
    fig = px.bar(
        df,
        x=bar_config["x_axis"]["column"],
        y=bar_config["y_axis"]["column"],
        color=bar_config["group_by"],
        title=bar_config["chart_title"],
        labels={
            bar_config["x_axis"]["column"]: data_config["headers"][bar_config["x_axis"]["column"]],
            bar_config["y_axis"]["column"]: data_config["headers"][bar_config["y_axis"]["column"]],
            bar_config["group_by"]: data_config["headers"][bar_config["group_by"]]
        },
        barmode='group'  # Group bars for each year by area
    )
    st.plotly_chart(fig, use_container_width=True)
