import datetime
import json
import os

import requests
from rich import print

CLI_DIR = os.path.join(os.path.expanduser("~"), ".cg_cli")
# trunk-ignore(bandit/B105)
TOKEN_BASE_FILEPATH = "tokens.json"
# trunk-ignore(bandit/B105)
TOKEN_LIST_URL = "https://api.coingecko.com/api/v3/coins/list"

def get_tokens() -> dict:
    return requests.get(TOKEN_LIST_URL, timeout=10).json()

def sync_tokens_to_local_storage() -> dict:
    file_path = os.path.join(CLI_DIR, TOKEN_BASE_FILEPATH)
    tokens = get_tokens()
    last_sync = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    token_data = {
        "tokens": tokens,
        "last_sync": last_sync,
    }
    os.makedirs(CLI_DIR, exist_ok=True)
    with open(file_path, "w") as file:
        json.dump(token_data, file, indent=4)
    print(f"Synced tokens to local storage [underline]{file_path}[/underline]: {last_sync}")
    return token_data

def read_tokens_to_local_storage() -> dict:
    file_path = os.path.join(CLI_DIR, TOKEN_BASE_FILEPATH)
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return sync_tokens_to_local_storage()