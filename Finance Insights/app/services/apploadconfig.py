from __future__ import annotations

import configparser
import json
from pathlib import Path
from typing import Any


JSON_PREFIX = "_json_val::"


def _convert_value(value: str) -> Any:
    value = value.strip()

    if value.startswith(JSON_PREFIX):
        return json.loads(value[len(JSON_PREFIX):])

    return value


def _get_config_directory() -> Path:
    return (Path(__file__).parent / "../../config").resolve()


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
    config_dir = _get_config_directory()

    configs = [
        _get_file_config(file)
        for file in sorted(config_dir.glob("*.ini"))
    ]

    return _merge_configs(configs)


config = load_config()