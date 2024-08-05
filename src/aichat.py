# -*- coding: utf-8 -*-

import argparse
import json
import os
import sys
import threading
import time
from rich.console import Console
from rich.spinner import Spinner
from src.conversation_manager import load_conversations, save_conversations
from src.openai_client import initialize_openai, get_completion
from src.styles import Color, Format, Style, Emoji
from rich.progress import Progress, BarColumn
from src.process import process

console = Console()

def display_loading_animation(stop_event):
    with console.status("Bot-aichat typing...", spinner="dots") as status:
        while not stop_event.is_set():
            time.sleep(0.1)

def get_response_with_loading(context, model):
    stop_event = threading.Event() 

    loading_thread = threading.Thread(target=display_loading_animation, args=(stop_event,))
    loading_thread.start()

    try:
        response = get_completion(context, model)
    finally:
        stop_event.set()
        loading_thread.join()
    return response

def handle_error(error):
    print("")
    print(Style.ERROR + Emoji.ERROR + " err-aichat ↴\n" + Format.END)
    print(error)
    print("")

def ask_to_continue(conversation_id):
    while True:
        user_input = console.input(f"Conversation with the identifier '{conversation_id}' already exists. Do you want to continue the existing conversation? (Y/n): ").strip().lower()
        if user_input in ['y', 'n', '']:
            return user_input != 'n'
        console.print("Please answer 'y[yes]' or 'n[no]'.")

def main(config):
    api_key = config.get("api_key")
    api_job = config.get("api_job")

    parser = argparse.ArgumentParser(description="AI Chat CLI")
    parser.add_argument("-k", "--api_key", type=str, help="OpenAI API Key", default=api_key)
    parser.add_argument("-m", "--message", type=str, help="Initial message to send to AI Chat")
    parser.add_argument("-p", "--prompt", type=str, help="Initial prompt to configure the AI Chat", default=api_job)
    parser.add_argument("-c", "--command", type=str, help="Command to be executed immediately")
    parser.add_argument("-f", "--file", type=str, help="Send the contents of a text file")
    parser.add_argument("--new", type=str, help="Start a new conversation with an identifier", default="default")
    parser.add_argument("--set", type=str, help="Continue an existing conversation with an identifier", default="dafault")
    parser.add_argument("--list", action='store_true', help="List all conversations")
    args = parser.parse_args()

    prompt = args.prompt
    api_key = args.api_key

    if not args.api_key:
        console.print("Please provide the OpenAI API key using the -k argument or set the OPENAI_API_KEY environment variable.")
        return

    initialize_openai(args.api_key)
    conversations = load_conversations()

    brain = "gpt"
    model = "gpt-4o"
    model_version = "4o"

    console.print("======= AI Chat CLI =======")
    console.print("Brain:", brain.upper())
    console.print("Model:", brain.upper()+"-"+model_version)
    console.print("Job:", "'"+prompt+"'")
    console.print("")
    console.print("(typing 'exit()' for quit)")
    console.print("==========================")
    console.print("")

    if args.list:
        console.print("Available conversations:")
        for convo_id in conversations.keys():
            console.print(f"- {convo_id}")
        return

    if args.new:
        conversation_id = args.new
        if conversation_id in conversations:
            if ask_to_continue(conversation_id):
                args.set = conversation_id
                args.new = None
            else:
                console.print("Operation cancelled. Please provide a different identifier to start a new conversation.")
                return
        else:
            context = [{"role": "system", "content": args.prompt}]
            conversations[conversation_id] = context
            console.print(f"New conversation '{conversation_id}' started.")

    if args.set:
        conversation_id = args.set
        if conversation_id not in conversations:
            console.print(f"Conversation with the identifier '{conversation_id}' not found.")
            args.new
            return
        context = conversations[conversation_id]
        console.print(f"Continuing conversation '{conversation_id}'.")

    if args.message:
        context.append({"role": "user", "content": args.message})
        try:
            response = get_completion(context, model)
            context.append({"role": "assistant", "content": response})
            print(Style.BOT + Emoji.BOT + " bot-aichat ↴" + Format.END)
            process(response)
            print("")
        except Exception as e:
            context.append({"role": "error", "content": str(e)})
            handle_error(e)

    if args.command:
        context.append({"role": "user", "content": args.command})
        try:
            response = get_completion(context, model)
            context.append({"role": "assistant", "content": response})
            print(Style.BOT + Emoji.BOT + " bot-aichat ↴" + Format.END)
            process(response)
            print("")
        except Exception as e:
            context.append({"role": "error", "content": str(e)})
            handle_error(e)

    if args.file:
        if os.path.exists(args.file):
            with open(args.file, "r") as file:
                file_content = file.read()
            context.append({"role": "user", "content": file_content})
            try:
                response = get_completion(context, model)
                context.append({"role": "assistant", "content": response})
                print(Style.BOT + Emoji.BOT + " bot-aichat ↴" + Format.END)
                process(response)
                print("")
            except Exception as e:
                context.append({"role": "error", "content": str(e)})
                handle_error(e)
        else:
            console.print(f"File '{args.file}' not found.")

    console.print("")
    console.print("==========================")
    console.print("           CHAT           ")
    console.print("==========================")

    while True:
        try:
            print(Style.USER + Emoji.USER + " user-aichat ↴" + Format.END)
            user_input = console.input()

            if user_input.lower() == "exit()":
                break

            if user_input.startswith("/show-prompt"):
                console.print(f"Current prompt: {prompt}")
                continue

            if user_input.startswith("/show-api_key"):
                console.print(f"Current api_key: {api_key}")
                continue

            if user_input.startswith("/nc"):
                user_input = user_input[len("/nc"):].strip()
                no_context = [{"role": "user", "content": user_input}]
                try:
                    print("")
                    response = get_response_with_loading(no_context, model)
                    no_context.append({"role": "assistant", "content": response})
                    print(Style.BOT + Emoji.BOT + " bot-aichat ↴" + Format.END + Color.PURPLE + " (no context)" + Format.END)
                    process(response)
                    print("")   
                except Exception as e:
                    no_context.append({"role": "error", "content": str(e)})
                    handle_error(e)

            else:
                context.append({"role": "user", "content": user_input})
                try:
                    print("")
                    response = get_response_with_loading(context, model)
                    context.append({"role": "assistant", "content": response})
                    print(Style.BOT + Emoji.BOT + " bot-aichat ↴" + Format.END)
                    process(response)
                    print("")   
                except Exception as e:
                    context.append({"role": "error", "content": str(e)})
                    handle_error(e)

        except Exception as e:
            handle_error(e)

    conversations[conversation_id] = context
    save_conversations(conversations)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        handle_error(e)
