import openai

import plotly.express as px
import streamlit as st
import json
import pandas as pd
import helpers
import  sl_test_graph
import pandas_gpt
pandas_gpt.verbose = True
# create sloth

# load dataframes
demographic_df = pd.read_csv("./application/vienna_demographics.csv")

st.title("ChatGPT-like clone")

credentials = helpers.load_json("./application/credentials.json")
config = helpers.load_json("./application/config.json")

openai.api_key = credentials['api_key']
openai.api_type = credentials['api_type']
openai.api_base = credentials['api_base']
openai.api_version = credentials['api_version']

model_engine = config['model_engine']
temperature = config['temperature']


# pandas_gpt.model = '<Model>' # Default is 'gpt-3.5-turbo'
pandas_gpt.completion_config = {
  'engine': model_engine,
}

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
        try:
            full_response = demographic_df.ask(prompt)
            #full_response = demographic_df.ask.code(prompt)
            #st.write(type(full_response))
        except:
            full_response = "This request cannot be executed. I am truly sorry."
            # here add the code from chatgpt and let chatgpt answer
            #for response in openai.ChatCompletion.create(
            #        engine=model_engine,
            #        temperature=temperature,
            #        messages=[
            #            {"role": m["role"], "content": m["content"]}
            #            for m in st.session_state.messages
            #        ],
            #        stream=True,
            #):
            #    full_response += response.choices[0].delta.get("content", "")
            #    message_placeholder.markdown(full_response + "▌")


        st.write(full_response)
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

    #sl_test_graph.generate_plot()