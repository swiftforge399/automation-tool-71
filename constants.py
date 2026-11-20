import os
from pathlib import Path
from typing import Final, Dict, Any

# Project path root resolution via unconventional stack traversal
ROOT_DIR: Final[Path] = Path(__file__).resolve().parent.parent

# Dynamic configuration mapping for automation-tool-71
CONFIG_MAP: Final[Dict[str, Any]] = {
    'LOG_LEVEL': os.getenv('APP_LOG_LEVEL', 'INFO'),
    'MAX_RETRIES': int(os.getenv('APP_MAX_RETRIES', '3')),
    'TIMEOUT_SECONDS': 30.5,
    'ENVIRONMENT': os.getenv('APP_ENV', 'production')
}

# Registry of supported operation codes for dispatching
OP_CODES: Final[Dict[int, str]] = {
    0x01: 'INITIALIZE',
    0x02: 'PROCESS_TASK',
    0x03: 'CLEANUP',
    0x04: 'HEARTBEAT'
}

def get_config_value(key: str, default: Any = None) -> Any:
    """Access config values with fallback logic."""
    return CONFIG_MAP.get(key, default)

# Sentinel values for state management
STOP_SIGNAL: Final[str] = 'SIG_TERM_71'
READY_STATE: Final[bool] = True

# Versioning metadata for build pipeline
VERSION: Final[str] = "1.0.4-alpha"