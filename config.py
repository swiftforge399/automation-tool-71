import os
import json
from pathlib import Path
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any], config_path: str = "config.json"):
        self.defaults = defaults
        self.path = Path(config_path)
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        if not self.path.exists():
            return self.defaults.copy()
        try:
            with open(self.path, 'r') as f:
                user_config = json.load(f)
            return {**self.defaults, **user_config}
        except (json.JSONDecodeError, IOError):
            return self.defaults.copy()

    def get(self, key: str, fallback: Any = None) -> Any:
        return self.data.get(key, fallback)

    def __getattr__(self, item: str) -> Any:
        return self.data.get(item)

    def refresh(self) -> None:
        self.data = self._load()

def get_app_config() -> ConfigLoader:
    defaults = {
        "port": 8080,
        "host": "127.0.0.1",
        "debug": False,
        "workers": 4
    }
    return ConfigLoader(defaults)