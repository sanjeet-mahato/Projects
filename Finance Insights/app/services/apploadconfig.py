from __future__ import annotations

import configparser
import json
from pathlib import Path
from typing import Any


JSON_PREFIX = "_json_val::"
JSON_FILE_PREFIX = "_json::"

PROJECT_ROOT = (Path(__file__).parent / "../..").resolve()
CONFIG_DIR = PROJECT_ROOT / "config"


def _convert_value(value: str) -> Any:
    value = value.strip()

    if value.startswith(JSON_PREFIX):
        return json.loads(value[len(JSON_PREFIX):])

    if value.startswith(JSON_FILE_PREFIX):
        file_path = PROJECT_ROOT / value[len(JSON_FILE_PREFIX):].strip()

        with file_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    return value


def _get_file_config(file: Path) -> dict[str, dict[str, Any]]:
    parser = configparser.ConfigParser()
    parser.read(file)

    return {
        section: {
            key: _convert_value(value)
            for key, value in parser.items(section)
        }
        for section in parser.sections()
    }


def _merge_configs(
    configs: list[dict[str, dict[str, Any]]],
) -> dict[str, dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}

    for config in configs:
        for section, values in config.items():
            merged.setdefault(section, {})

            conflict = merged[section].keys() & values.keys()
            if conflict:
                raise ValueError(
                    f"Duplicate configuration: "
                    f"{section}.{next(iter(conflict))}"
                )

            merged[section].update(values)

    return merged


def load_config() -> dict[str, dict[str, Any]]:
    configs = [
        _get_file_config(file)
        for file in sorted(CONFIG_DIR.glob("*.ini"))
    ]

    return _merge_configs(configs)


config = load_config()