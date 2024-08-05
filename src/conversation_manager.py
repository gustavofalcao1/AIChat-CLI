import json
import os

CONVERSATIONS_FILE = os.path.join(os.path.dirname(__file__), '../data/conversations.json')
CONVERSATIONS_FILE_LOG = os.path.join(os.path.dirname(__file__), '../data/log.json')

def load_conversations():
    if os.path.exists(CONVERSATIONS_FILE):
        with open(CONVERSATIONS_FILE, "r") as file:
            return json.load(file)
    return {}

def save_conversations(conversations):
    cleaned_conversations = {key: value for key, value in conversations.items() if not any(message.get('role') == 'error' for message in value)}
    with open(CONVERSATIONS_FILE, "w") as file:
        json.dump(cleaned_conversations, file)
    save_log(conversations)

def save_log(conversations):
    with open(CONVERSATIONS_FILE_LOG, "w") as file:
        json.dump(conversations, file)
