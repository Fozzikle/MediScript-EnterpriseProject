import json
import os

CONFIG_FILE = "config.json"


def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}


def base_folder():
    config = load_config()
    return config.get('base_folder', ' ')


def is_setup_completed():
    config = load_config()
    return config.get("setup_complete", False)


def get_base_folder():
    config_path = os.path.join(os.getcwd(), "config.json")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = json.load(f)
            return config.get("base_folder")
    return None
