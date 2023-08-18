import json
import re
import os
import pandas as pd
import pandasql as psql
import streamlit as st
import openai


# -------------------------
# Utility Functions
# -------------------------

def load_json(filename):
    """
    Load a JSON file.

    :param filename: Path to the JSON file
    :return: The content of the JSON file
    """
    with open(filename, 'r') as file:
        content = json.load(file)
    return content


def parse_sql_query(response):
    """
    Parse SQL query from the response.

    :param response: The response text
    :return: The SQL query if found, None otherwise
    """
    pattern = r'\'\'\'(.*?)\'\'\'|\"\"\"(.*?)\"\"\"'
    match = re.search(pattern, response, re.DOTALL)
    return match.group(1) or match.group(2) if match else None


def execute_sql_query_on_dataframe(sql_query, df):
    """
    Execute a SQL query on a Pandas DataFrame.

    :param sql_query: The SQL query string
    :param df: The Pandas DataFrame to query
    :return: The result of the SQL query as a DataFrame
    """
    return psql.sqldf(sql_query, locals())


def list_csv_files(directory):
    """
    List all CSV files in a given directory.

    :param directory: The directory path
    :return: A list of CSV file names in the directory
    """
    return [f for f in os.listdir(directory) if f.endswith('.csv')]


def load_csv_file(file_path):
    """
    Load a CSV file into a Pandas DataFrame.

    :param file_path: The path to the CSV file
    :return: A Pandas DataFrame containing the CSV data
    """
    return pd.read_csv(file_path)


# -------------------------
# Streamlit App
# -------------------------

st.title("ChatGPT-like clone")

# Set directory path
directory = './application/'

# List CSV files and select one via dropdown menu
csv_files = list_csv_files(directory)
selected_csv_file = st.selectbox('Wählen Sie eine CSV-Datei:', csv_files)

# Load selected CSV file
if st.button('Lade CSV Datei'):
    file_path = os.path.join(directory, selected_csv_file)
    st.session_state.df = load_csv_file(file_path)
    st.write(st.session_state.df)

# Load OpenAI model credentials and configuration
credentials = load_json("./application/credentials.json")
config = load_json("./application/config.json")

# Set OpenAI API credentials
openai.api_key = credentials['api_key']
openai.api_type = credentials['api_type']
openai.api_base = credentials['api_base']
openai.api_version = credentials['api_version']

# Chat initialization
model_engine = config['model_engine']
temperature = config['temperature']
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Hallo wie kann ich Ihnen helfen?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Process and display assistant message
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

        # Extract and apply SQL query from assistant response
        sql_query = parse_sql_query(full_response)
        if 'df' in st.session_state and sql_query:
            result = execute_sql_query_on_dataframe(sql_query, st.session_state.df)
            st.write(result)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
