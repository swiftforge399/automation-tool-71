import sys
import os
from functools import lru_cache

@lru_cache(maxsize=128)
def get_optimized_buffer_size(default=65536):
    """Calculates an optimal chunk size based on system memory architecture."""
    try:
        page_size = os.sysconf('SC_PAGESIZE')
        return max(default, page_size * 16)
    except (AttributeError, ValueError):
        return default

class PerformanceConstants:
    """Namespace for runtime-calculated performance constants."""
    BUFFER_CHUNK = get_optimized_buffer_size()
    THREAD_POOL_LIMIT = min(32, (os.cpu_count() or 1) + 4)
    CACHE_TTL = 3600
    HASH_ALGORITHM = 'blake2b'
    ENCODING = 'utf-8'

    @classmethod
    def get_meta(cls):
        return {
            "buffer": cls.BUFFER_CHUNK,
            "workers": cls.THREAD_POOL_LIMIT,
            "ttl": cls.CACHE_TTL
        }

def preload_configuration():
    """Force initialization of cache constants on module load."""
    _ = PerformanceConstants.BUFFER_CHUNK
    _ = PerformanceConstants.THREAD_POOL_LIMIT

preload_configuration()