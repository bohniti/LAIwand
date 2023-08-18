import streamlit as st
import os
import openai
from pathlib import Path
from daten_laden import list_csv_files, load_csv_file
from daten_visualisieren import generate_plotly_plot
from query_intent_confirmation import ask_for_intent_confirmation
from utility_functions import load_json, parse_sql_query, execute_sql_query_on_dataframe

def main():
    st.title("ChatGPT-like clone")

    directory = Path("LAIwand/application/").resolve()
    csv_files = list_csv_files(directory)
    selected_csv_file = st.selectbox('Wählen Sie eine CSV-Datei:', csv_files)

    if st.button('Lade CSV Datei'):
        file_path = os.path.join(directory, selected_csv_file)
        st.session_state.df = load_csv_file(file_path)
        st.write(st.session_state.df)

    credentials = load_json(Path("LAIwand/application/credentials.json").resolve())
    config = load_json(Path("LAIwand/application/config.json").resolve())

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

        if st.button("Deny the above intent"):
            st.session_state.intent_confirmed = False
            st.session_state.prompt = None
            st.session_state.messages = []
            st.chat_input("Intent denied. Please try again. How can I assist you?")

    if st.session_state.prompt and st.session_state.intent_confirmed:
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

            if 'plot' in st.session_state.prompt.lower():
                if 'df' in st.session_state:
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

if __name__ == "__main__":
    main()
