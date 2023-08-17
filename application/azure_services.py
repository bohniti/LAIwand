import openai
import json


def load_credentials(filename="./application/credentials.json"):
    with open(filename, 'r') as file:
        credentials = json.load(file)
    return credentials


def load_config(filename="./application/config.json"):
    with open(filename, 'r') as file:
        config = json.load(file)
    return config


def create_response(user_prompt):
    credentials = load_credentials()
    config = load_config()

    openai.api_type = credentials['api_type']
    openai.api_base = credentials['api_base']
    openai.api_version = credentials['api_version']
    openai.api_key = credentials['api_key']

    model_engine = config['model_engine']
    temperature = config['temperature']
    n = config['n']

    response = openai.ChatCompletion.create(
        engine=model_engine,
        temperature=temperature,
        n=n,
        messages=[
            {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
            {"role": "user", "content": user_prompt}
        ]
    )

    return response


# Example Usage
user_prompt = "Tell me a joke"
response = create_response(user_prompt)
print(response)
