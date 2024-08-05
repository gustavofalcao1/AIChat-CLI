import os
import json
import src.aichat

def load_config():
    if os.path.exists("data/config.json"):
        with open("data/config.json", "r") as arquivo:
            config = json.load(arquivo)
            return config
    else:
        return {}

def save_config(config):
    with open("data/config.json", "w") as arquivo:
        json.dump(config, arquivo)

def create_conversations(api_job):
    default_conversation = {"default": [{"role": "system", "content": api_job}]}
    with open("data/conversations.json", "w") as arquivo:
        json.dump(default_conversation, arquivo, indent=4)

def get_config():
    api_key = input("Enter your Key Api: ")
    api_job = input("Enter the API work: ")
    config = {"api_key": api_key, "api_job": api_job}
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
