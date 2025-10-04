import os
import json


def load_json_config(file_name: str) -> dict:
    """
    Loads a JSON configuration file and returns it as a dictionary.

    Args:
        file_name (str): Name of the JSON file (with relative path)

    Returns:
        dict: Dictionary containing the JSON config values
    """
    file_path = os.path.join(os.path.dirname(__file__), "..", "config", file_name)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Config file not found: {file_path}")

    with open(file_path, "r") as f:
        config_data = json.load(f)

    return config_data
