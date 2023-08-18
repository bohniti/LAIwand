import json
import re
import pandas as pd
import pandasql as psql
import os
import pandas as pd
import streamlit as st

def load_json(filename):
    with open(filename, 'r') as file:
        credentials = json.load(file)
    return credentials

def parse_sql_query(response):
    # Regular expression pattern for matching SQL statements enclosed in triple quotes
    pattern = r'\'\'\'(.*?)\'\'\'|\"\"\"(.*?)\"\"\"'

    # Search for the pattern in the response
    match = re.search(pattern, response, re.DOTALL)

    # If a match is found, return the SQL statement, otherwise return None
    if match:
        return match.group(1) or match.group(2)
    else:
        return None

def execute_sql_query_on_dataframe(sql_query, df):
    """
    Load a Pandas DataFrame from a file and execute a SQL query on it.

    Parameters:
    file_path (str): The file path to load the DataFrame from (e.g., a CSV file).
    sql_query (str): The SQL query to be executed on the DataFrame.

    Returns:
    pd.DataFrame: The result of the SQL query executed on the loaded DataFrame.
    """

    # Load the DataFrame from the file
    # Here we assume that the file is in CSV format.
    # For other file formats like Excel, use pd.read_excel instead of pd.read_csv
    #df = pd.read_csv(file_path)

    # Execute the SQL query on the loaded DataFrame
    result = psql.sqldf(sql_query, locals())

    return result


def wrap_user_prompt(user_prompt, start_hidden_prompt, end_hidden_prompt):
    """
    Wrap the user prompt with hidden system prompts at the beginning and the end.

    Parameters:
    user_prompt (str): The actual user input prompt string.
    start_hidden_prompt (str): The hidden system prompt to be added at the beginning.
    end_hidden_prompt (str): The hidden system prompt to be added at the end.

    Returns:
    str: The wrapped prompt string.
    """
    wrapped_prompt = f'[SYSTEM]{start_hidden_prompt}[/SYSTEM][USER]{user_prompt}[/USER][SYSTEM]{end_hidden_prompt}[/SYSTEM]'
    return wrapped_prompt


def list_csv_files(directory):
    """
    Diese Funktion gibt eine Liste aller .csv-Dateien in einem gegebenen Verzeichnis zurück.
    :param directory: Das Verzeichnis, in dem nach .csv-Dateien gesucht werden soll.
    :return: Eine Liste der Pfade aller .csv-Dateien im angegebenen Verzeichnis.
    """
    return [f for f in os.listdir(directory) if f.endswith('.csv')]

def load_csv_file(file_path):
    """
    Diese Funktion lädt eine .csv-Datei in einen Pandas DataFrame.
    :param file_path: Der Pfad zur .csv-Datei.
    :return: Ein Pandas DataFrame, der die Daten aus der .csv-Datei enthält.
    """
    return pd.read_csv(file_path)