import sys
import time
from collections import deque
from threading import Lock

class AsyncPerformanceLogger:
    def __init__(self, capacity=1000):
        self._buffer = deque(maxlen=capacity)
        self._lock = Lock()
        self._last_flush = time.monotonic()

    def log(self, message):
        timestamp = time.monotonic()
        self._buffer.append(f"[{timestamp:.4f}] {message}")
        if len(self._buffer) >= self._buffer.maxlen or (timestamp - self._last_flush) > 5.0:
            self.flush()

    def flush(self):
        with self._lock:
            if not self._buffer:
                return
            batch = list(self._buffer)
            self._buffer.clear()
            self._last_flush = time.monotonic()
            sys.stdout.write("\n".join(batch) + "\n")
            sys.stdout.flush()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.flush()