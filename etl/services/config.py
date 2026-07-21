import json
import os
from pathlib import Path


class Config:

    _cache = {}

    @classmethod
    def get_environment(cls):
        return os.getenv("APP_ENV", "development")

    @classmethod
    def load(cls, filename):

        environment = cls.get_environment()

        cache_key = (environment, filename)

        if cache_key in cls._cache:
            return cls._cache[cache_key]

        config_path = (
            Path("/app/config")
            / environment
            / filename
        )

        with open(config_path, "r") as f:
            config = json.load(f)

        cls._cache[cache_key] = config

        return config