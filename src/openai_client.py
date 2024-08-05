import os
from openai import OpenAI

client = None

def initialize_openai(api_key):
    global client
    client = OpenAI(api_key=api_key)


def get_completion(messages, model):
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    return response.choices[0].message.content
