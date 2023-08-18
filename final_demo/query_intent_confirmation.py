import openai

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
