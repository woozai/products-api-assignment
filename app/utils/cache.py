from typing import Any

from app.cache import CACHE_TTL_SECONDS, MemoryCacheBackend

default_cache_backend = MemoryCacheBackend()


def build_products_cache_key(api_mode: str, *, query: str = "", limit: int, skip: int) -> str:
    """Build a stable cache key for product listing and search requests."""
    normalized_query = query.strip().lower()
    return f"products:{api_mode}:q={normalized_query}:limit={limit}:skip={skip}"


def get_cached_value(cache_key: str) -> Any | None:
    """Read from the default in-memory cache backend."""
    return default_cache_backend.get(cache_key)


def set_cached_value(cache_key: str, value: Any, ttl_seconds: int = CACHE_TTL_SECONDS) -> None:
    """Write to the default in-memory cache backend."""
    default_cache_backend.set(cache_key, value, ttl_seconds)
