import re
from typing import Any, Dict, Callable

class DataValidator:
    def __init__(self):
        self.rules = {
            "id": lambda x: isinstance(x, int) and x > 0,
            "payload": lambda x: isinstance(x, str) and len(x) < 1024,
            "timestamp": lambda x: isinstance(x, (int, float))
        }

    def validate(self, data: Dict[str, Any]) -> bool:
        try:
            return all(self.rules[k](v) for k, v in data.items() if k in self.rules)
        except Exception:
            return False

class SchemaError(Exception):
    pass

def validate_payload(func: Callable):
    def wrapper(*args, **kwargs):
        data = args[0] if args else kwargs.get("data")
        validator = DataValidator()
        if not validator.validate(data):
            raise SchemaError(f"Invalid input structure detected: {data}")
        return func(*args, **kwargs)
    return wrapper

def sanitize_input(data: Dict[str, Any]) -> Dict[str, Any]:
    return {k: re.sub(r'[^\w\s]', '', str(v)) for k, v in data.items()}