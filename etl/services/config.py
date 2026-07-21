import json
from pathlib import Path


class Config:

    _cache = {}

    CONFIG_DIR = Path("/app/config")

    @classmethod
    def load(cls, filename):

        if filename in cls._cache:
            return cls._cache[filename]

        filepath = cls.CONFIG_DIR / filename

        with open(filepath, "r") as f:
            config = json.load(f)

        cls._cache[filename] = config

        return config