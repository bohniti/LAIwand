import openai
import streamlit as st
import json

def load_credentials(filename="./application/credentials.json"):
    with open(filename, 'r') as file:
        credentials = json.load(file)
    return credentials


def load_config(filename="./application/config.json"):
    with open(filename, 'r') as file:
        config = json.load(file)
    return config

st.title("ChatGPT-like clone")

openai.api_key = "ec6b8771460d416aa289f4e1748851be"
credentials = load_credentials()
config = load_config()

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

if prompt := st.chat_input("What is up?"):
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