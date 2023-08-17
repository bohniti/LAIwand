import openai

import plotly.express as px
import streamlit as st
import json
import pandas as pd
import helpers


st.title("ChatGPT-like clone")

openai.api_key = "ec6b8771460d416aa289f4e1748851be"
credentials = helpers.load_json("./application/credentials.json")
config = helpers.load_json("./application/config.json")

openai.api_type = credentials['api_type']
openai.api_base = credentials['api_base']
openai.api_version = credentials['api_version']
openai.api_key = credentials['api_key']

model_engine = config['model_engine']
temperature = config['temperature']

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Hallo wie kann ich Ihnen helfen?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            engine=model_engine,
            temperature=temperature,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})



# Load data and configuration from the JSON files
with open('./application/sl_graph_data.json', 'r') as data_file:
    data_config = json.load(data_file)

with open('./application/sl_graph_hist_config.json', 'r') as hist_file:
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
