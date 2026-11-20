import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any] = None):
        self._config = defaults or {}

    def __getitem__(self, key: str) -> Any:
        return self._config.get(key)

    def load_from_json(self, path: str) -> None:
        if not os.path.exists(path):
            return
        try:
            with open(path, 'r') as f:
                file_data = json.load(f)
                self._config.update({k: v for k, v in file_data.items() if v is not None})
        except (json.JSONDecodeError, IOError):
            pass

    def hydrate(self, env_prefix: str = 'APP_') -> None:
        for key in self._config.keys():
            env_val = os.getenv(f"{env_prefix}{key.upper()}")
            if env_val:
                # Attempt type inference based on default
                default_type = type(self._config[key])
                try:
                    self._config[key] = default_type(env_val)
                except (ValueError, TypeError):
                    self._config[key] = env_val

    def to_dict(self) -> Dict[str, Any]:
        return dict(self._config)

def get_app_config() -> ConfigLoader:
    defaults = {'port': 8080, 'debug': False, 'host': 'localhost'}
    loader = ConfigLoader(defaults)
    loader.load_from_json('settings.json')
    loader.hydrate()
    return loader