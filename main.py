import os
import json
import src.aichat

def load_config():
    config_path = os.path.expanduser("~/.aichat/config.json")
    if os.path.exists(config_path):
        with open(config_path, "r") as arquivo:
            config = json.load(arquivo)
            return config
    else:
        return {}

def save_config(config):
    config_path = os.path.expanduser("~/.aichat/config.json")
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, "w") as arquivo:
        json.dump(config, arquivo)

def create_conversations(api_job):
    conversations_path = os.path.expanduser("~/.aichat/conversations.json")
    os.makedirs(os.path.dirname(conversations_path), exist_ok=True)
    default_conversation = {"default": [{"role": "system", "content": api_job}]}
    with open(conversations_path, "w") as arquivo:
        json.dump(default_conversation, arquivo, indent=4)

def get_config():
    api_url = input("Enter the API URL (default: https://api.openai.com/v1): ") or "https://api.openai.com/v1"
    api_key = input("Enter your API Key: ")
    api_model = input("Enter the API model (default: openai/gpt-4o): ") or "openai/gpt-4o"
    api_job = input("Enter the API job: ")
    config = {"api_url": api_url,"api_key": api_key, "api_job": api_job, "api_model": api_model}
    save_config(config)
    create_conversations(api_job)
    return config

def main():
    config = load_config()
    if not config:
        print("Configurations not found. Please enter the settings.")
        print("")
        config = get_config()

    src.aichat.main(config)

if __name__ == "__main__":
    main()
