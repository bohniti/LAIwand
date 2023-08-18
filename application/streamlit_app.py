import json
import re
import os
import pandas as pd
import pandasql as psql
import streamlit as st
import openai
import plotly.express as px


# -------------------------
# Utility Functions
# -------------------------

def load_json(filename):
    with open(filename, 'r') as file:
        content = json.load(file)
    return content


def parse_sql_query(response):
    pattern = r'\'\'\'(.*?)\'\'\'|\"\"\"(.*?)\"\"\"'
    match = re.search(pattern, response, re.DOTALL)
    return match.group(1) or match.group(2) if match else None


def execute_sql_query_on_dataframe(sql_query, df):
    return psql.sqldf(sql_query, locals())


def list_csv_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.csv')]


def load_csv_file(file_path):
    return pd.read_csv(file_path)


def ask_for_intent_confirmation(prompt, model_engine, temperature):
    intent_response = openai.ChatCompletion.create(
        engine=model_engine,
        temperature=temperature,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    intent_text = intent_response.choices[0].message.get("content", "Do you mean: ...?")
    return intent_text

# Neue Funktion, um einen Plotly-Plot zu erstellen
def generate_plotly_plot(df):
    fig = px.scatter(df, x=df.columns[0], y=df.columns[1])
    return fig


# -------------------------
# Streamlit App
# -------------------------

st.title("ChatGPT-like clone")

directory = './application/'

csv_files = list_csv_files(directory)
selected_csv_file = st.selectbox('Wählen Sie eine CSV-Datei:', csv_files)

if st.button('Lade CSV Datei'):
    file_path = os.path.join(directory, selected_csv_file)
    st.session_state.df = load_csv_file(file_path)
    st.write(st.session_state.df)

credentials = load_json("./application/credentials.json")
config = load_json("./application/config.json")

openai.api_key = credentials['api_key']
openai.api_type = credentials['api_type']
openai.api_base = credentials['api_base']
openai.api_version = credentials['api_version']

model_engine = config['model_engine']
temperature = config['temperature']
if "messages" not in st.session_state:
    st.session_state.messages = []
if 'intent_confirmed' not in st.session_state:
    st.session_state.intent_confirmed = False
if 'prompt' not in st.session_state:
    st.session_state.prompt = None

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if not st.session_state.prompt:
    st.session_state.prompt = st.chat_input("Hallo wie kann ich Ihnen helfen?")

if st.session_state.prompt and not st.session_state.intent_confirmed:
    intent_text = ask_for_intent_confirmation(st.session_state.prompt, model_engine, temperature)
    st.session_state.messages.append({"role": "user", "content": st.session_state.prompt})
    with st.chat_message("assistant"):
        st.markdown(intent_text)

    if st.button("Confirm the above intent"):
        st.session_state.intent_confirmed = True

if st.session_state.intent_confirmed:
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

        # Prüfen, ob das Wort 'plot' in der Anfrage des Nutzers vorkommt
        if 'plot' in st.session_state.prompt.lower():
            if 'df' in st.session_state:
                # Erstellen und Anzeigen des Plotly-Plots
                fig = generate_plotly_plot(st.session_state.df)
                st.plotly_chart(fig)
        else:
            sql_query = parse_sql_query(full_response)
            if 'df' in st.session_state and sql_query:
                result = execute_sql_query_on_dataframe(sql_query, st.session_state.df)
                st.write(result)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.session_state.intent_confirmed = False
    st.session_state.prompt = None
    st.session_state.messages = []

