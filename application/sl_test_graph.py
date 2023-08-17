import openai
import plotly.express as px
import streamlit as st
import pandas as pd
import helpers

def generate_plot():
    
    # Should be passed to function
    graph_type = "bar"  
    #graph_type = "clustered_bar"  
    
    if graph_type == "bar":
        plot_config_path = "./application/sl_graph_config/sl_graph_bar_config.json"
        data_path = "./application/sl_graph_config/sl_graph_data.json"
    elif graph_type == "clustered_bar":
        plot_config_path = "./application/sl_graph_config/sl_graph_clustered_bar_config.json"
        data_path = "./application/sl_graph_config/sl_graph_clustered_bar_data.json"

    plot_config = helpers.load_json(plot_config_path)
    data_config = helpers.load_json(data_path)
    
    # Convert data to DataFrame
    df = pd.DataFrame(data_config["data"])

    # Generate the appropriate plot based on the graph_type
    if graph_type == "bar":
        fig = px.bar(
            df,
            x=plot_config["x_axis"]["column"],
            y=plot_config["y_axis"]["column"],
            color=plot_config["group_by"],
            title=plot_config["chart_title"],
            labels={
                plot_config["x_axis"]["column"]: data_config["headers"][plot_config["x_axis"]["column"]],
                plot_config["y_axis"]["column"]: data_config["headers"][plot_config["y_axis"]["column"]],
                plot_config["group_by"]: data_config["headers"][plot_config["group_by"]]
            },
            barmode='group'
        )
    
    elif graph_type == "clustered_bar":
        fig = px.bar(
            df,
            x=plot_config["x_axis"]["column"],
            y=[col for col in plot_config["y_columns"]],
            color=plot_config["group_by"],
            title=plot_config["chart_title"],
            labels={col: data_config["headers"][col] for col in [plot_config["x_axis"]["column"], *plot_config["y_columns"], plot_config["group_by"]]},
            barmode='group'
        )
    
    st.title(plot_config["chart_title"])
    st.plotly_chart(fig, use_container_width=True)
