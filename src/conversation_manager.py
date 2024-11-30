import json
import os
import sys

def get_data_file_path(filename):
    if getattr(sys, 'frozen', False):
        # Executando como um executável gerado pelo PyInstaller
        base_path = os.path.expanduser("~/.aichat")
    else:
        # Executando como um script Python normal
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, filename)

CONVERSATIONS_FILE = get_data_file_path('conversations.json')
CONVERSATIONS_FILE_LOG = get_data_file_path('log.json')

def ensure_data_dir_exists():
    data_dir = os.path.dirname(CONVERSATIONS_FILE)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

def load_conversations():
    if os.path.exists(CONVERSATIONS_FILE):
        with open(CONVERSATIONS_FILE, "r") as file:
            return json.load(file)
    return {}

def save_conversations(conversations):
    ensure_data_dir_exists()
    cleaned_conversations = {key: value for key, value in conversations.items() if not any(message.get('role') == 'error' for message in value)}
    with open(CONVERSATIONS_FILE, "w") as file:
        json.dump(cleaned_conversations, file)
    save_log(conversations)

def save_log(conversations):
    with open(CONVERSATIONS_FILE_LOG, "w") as file:
        json.dump(conversations, file)
