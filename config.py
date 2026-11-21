import os
import json
from collections import ChainMap
from pathlib import Path
from typing import Any, Dict


class ConfigNamespace:
    """Dynamic dot-notation wrapper around nested dict/ChainMap configuration structures."""

    def __init__(self, *maps: Dict[str, Any]):
        self._data = ChainMap(*maps)

    def __getattr__(self, item: str) -> Any:
        if item.startswith("_"):
            raise AttributeError(item)
        val = self._data.get(item)
        if isinstance(val, dict):
            return ConfigNamespace(val)
        if val is None:
            raise AttributeError(f"Configuration key '{item}' not found")
        return val

    def get(self, item: str, default: Any = None) -> Any:
        try:
            return getattr(self, item)
        except AttributeError:
            return default


DEFAULTS: Dict[str, Any] = {
    "app_name": "automation-tool-71",
    "debug": False,
    "max_retries": 3,
    "timeout": 30.0,
    "paths": {"output": "./output", "logs": "./logs"},
}


def load_config(config_path: str | Path | None = None) -> ConfigNamespace:
    """Loads configuration combining environment variables, file overrides, and hardcoded defaults."""
    file_override: Dict[str, Any] = {}
    if config_path and Path(config_path).exists():
        with open(config_path, "r", encoding="utf-8") as f:
            file_override = json.load(f)

    env_override: Dict[str, Any] = {}
    for key in DEFAULTS:
        env_var = f"APP_{key.upper()}"
        if env_var in os.environ:
            raw_val = os.environ[env_var]
            default_type = type(DEFAULTS[key])
            if default_type == bool:
                env_override[key] = raw_val.lower() in ("true", "1", "yes")
            elif default_type in (int, float):
                env_override[key] = default_type(raw_val)
            else:
                env_override[key] = raw_val

    return ConfigNamespace(env_override, file_override, DEFAULTS)
