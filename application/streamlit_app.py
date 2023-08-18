import openai
import streamlit as st
import os
import pandas as pd
import helpers

# Deine Helper-Methoden können hier importiert werden, z.B.
#from helpers import list_csv_files, load_csv_file, load_json, parse_sql_query, execute_sql_query_on_dataframe

st.title("ChatGPT-like clone")

# Setzen Sie Ihr Verzeichnis hier
directory = './application/'

# Liste der .csv-Dateien im Verzeichnis
csv_files = helpers.list_csv_files(directory)

# Dropdown zur Auswahl einer .csv-Datei
selected_csv_file = st.selectbox('Wählen Sie eine CSV-Datei:', csv_files)

# Button zum Laden der ausgewählten .csv-Datei
if st.button('Lade CSV Datei'):
    # Der vollständige Pfad zur ausgewählten .csv-Datei
    file_path = os.path.join(directory, selected_csv_file)

    # Laden der .csv-Datei in einen Pandas DataFrame und Speichern im session_state
    st.session_state.df = helpers.load_csv_file(file_path)

    # Anzeigen des geladenen DataFrames
    st.write(st.session_state.df)

# Initialisierung des OpenAI-Modells
credentials = helpers.load_json("./application/credentials.json")
config = helpers.load_json("./application/config.json")

openai.api_key = credentials['api_key']
openai.api_type = credentials['api_type']
openai.api_base = credentials['api_base']
openai.api_version = credentials['api_version']

model_engine = config['model_engine']
temperature = config['temperature']

# Initialisieren des Chats
if "messages" not in st.session_state:
    st.session_state.messages = []

# Anzeigen der Chat-Nachrichten
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input-Feld für den Benutzer
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

        # SQL-Query aus der Antwort des Assistenten extrahieren
        sql_query = helpers.parse_sql_query(full_response)

        # Die SQL-Query auf den geladenen DataFrame anwenden, falls einer vorhanden ist
        if 'df' in st.session_state:
            result = helpers.execute_sql_query_on_dataframe(sql_query, st.session_state.df)
            st.write(result)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
