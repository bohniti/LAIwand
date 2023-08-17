import json
import re
import pandas as pd
import git  as psql

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

def execute_sql_query_on_dataframe(file_path, sql_query):
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
    df = pd.read_csv(file_path)

    # Execute the SQL query on the loaded DataFrame
    result = psql.sqldf(sql_query, locals())

    return result