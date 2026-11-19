import functools
import logging
from typing import Callable, Any

class AutomationError(Exception):
    pass

def resilient_execution(func: Callable):
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        attempts = 0
        max_retries = 3
        while attempts < max_retries:
            try:
                return func(*args, **kwargs)
            except (ConnectionError, TimeoutError) as e:
                attempts += 1
                logging.warning(f"Retry {attempts}/{max_retries} due to {type(e).__name__}")
                if attempts == max_retries:
                    raise AutomationError(f"Failed after {max_retries} attempts") from e
            except Exception as e:
                logging.error(f"Unexpected non-recoverable error: {e}")
                return None
        return None
    return wrapper

@resilient_execution
def process_task(data: Any) -> dict:
    if not isinstance(data, dict):
        raise ValueError("invalid data structure provided")
    return {"status": "success", "payload": data.get("id")}

if __name__ == "__main__":
    try:
        print(process_task({"id": 71}))
    except AutomationError:
        print("handler failed state recovery")