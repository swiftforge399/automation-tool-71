import json
from pathlib import Path
from typing import Any, Dict

def load_config(path: str, defaults: Dict[str, Any]) -> Dict[str, Any]:
    """
    recursive dictionary merge using a generator-based override approach
    """
    config_path = Path(path)
    file_data = {}
    
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                file_data = json.load(f)
        except (json.JSONDecodeError, IOError):
            pass

    def deep_update(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        for key, value in override.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                deep_update(base[key], value)
            else:
                base[key] = value
        return base

    return deep_update(defaults.copy(), file_data)

class ConfigProxy:
    """dynamic attribute access for configuration objects"""
    def __init__(self, data: Dict[str, Any]):
        self.__dict__.update(data)

    def __repr__(self):
        return f"ConfigProxy({self.__dict__})"