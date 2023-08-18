import json
import re
import pandasql as psql

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
