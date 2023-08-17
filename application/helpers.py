import json
def load_json(filename):
    with open(filename, 'r') as file:
        credentials = json.load(file)
    return credentials