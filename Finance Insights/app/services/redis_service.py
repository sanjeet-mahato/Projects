import json
from typing import Any

import redis

from app.services.apploadconfig import config


class RedisService:
    def __init__(self):
        redis_config = config["redis"]

        connection = {
            "host": redis_config["host"],
            "port": redis_config["port"],
            "db": redis_config["db"],
            "password": redis_config.get("password"),
        }

        self.client = redis.Redis(**connection)
        self.default_ttl = redis_config["default_ttl"]

    def ping(self) -> bool:
        return self.client.ping()

    def set(self, key: str, value: Any, ttl: int | None = None) -> bool:
        ttl = self.default_ttl if ttl is None else ttl
        return self.client.set(key, value, ex=ttl)

    def get(self, key: str) -> str | None:
        value = self.client.get(key)

        if value is None:
            return None

        return value.decode("utf-8")

    def delete(self, key: str) -> int:
        return self.client.delete(key)

    def set_json(self, key: str, value: Any, ttl: int | None = None) -> bool:
        return self.set(key, json.dumps(value), ttl)

    def get_json(self, key: str) -> Any | None:
        value = self.get(key)

        if value is None:
            return None

        return json.loads(value)

    def scan(self, pattern: str = "*") -> list[str]:
        return [key.decode("utf-8") for key in self.client.scan_iter(match=pattern)]

    def info(self) -> dict[str, Any]:
        return self.client.info()
