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


def write_json_config(file_name: str, data: dict | list, indent: int = 4) -> bool:
    """
    Writes a dictionary or list into a JSON file in the '../config/' folder.

    Args:
        file_name (str): Name of the JSON file (e.g., 'headers.json').
        data (dict | list): Python object to convert & persist.
        indent (int): Number of spaces for indentation (default 4).

    Returns:
        bool: True if write succeeded, False otherwise.
    """
    if not isinstance(data, (dict, list)):
        raise TypeError(f"Expected data to be dict or list, got {type(data).__name__}")

    try:
        file_path = os.path.join(os.path.dirname(__file__), "..", "config", file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w") as f:
            json.dump(data, f, indent=indent)

        return True

    except Exception as e:
        print(f"Error writing JSON file → {e}")
        return False
