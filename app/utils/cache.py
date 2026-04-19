import logging
from dataclasses import dataclass
from time import monotonic
from typing import Any

CACHE_TTL_SECONDS = 60
MAX_CACHE_ENTRIES = 128

logger = logging.getLogger(__name__)


@dataclass
class CacheEntry:
    """Value stored in the in-memory cache with its expiration time."""

    value: Any
    expires_at: float


_cache_entries: dict[str, CacheEntry] = {}


def build_products_cache_key(api_mode: str, *, query: str = "", limit: int, skip: int) -> str:
    """Build a stable cache key for product listing and search requests."""
    normalized_query = query.strip().lower()
    return f"products:{api_mode}:q={normalized_query}:limit={limit}:skip={skip}"


def get_cached_value(cache_key: str) -> Any | None:
    """Return a cached value when it exists and has not expired."""
    cache_entry = _cache_entries.get(cache_key)

    if cache_entry is None:
        logger.info("Cache miss: %s", cache_key)
        return None

    if cache_entry.expires_at <= monotonic():
        del _cache_entries[cache_key]
        logger.info("Cache expired: %s", cache_key)
        return None

    logger.info("Cache hit: %s", cache_key)
    return cache_entry.value


def set_cached_value(cache_key: str, value: Any, ttl_seconds: int = CACHE_TTL_SECONDS) -> None:
    """Store a value in memory for a short time."""
    _remove_expired_entries()

    if cache_key not in _cache_entries and len(_cache_entries) >= MAX_CACHE_ENTRIES:
        oldest_cache_key = next(iter(_cache_entries))
        del _cache_entries[oldest_cache_key]
        logger.info("Cache full, removed oldest entry: %s", oldest_cache_key)

    _cache_entries[cache_key] = CacheEntry(
        value=value,
        expires_at=monotonic() + ttl_seconds,
    )
    logger.info("Cache stored: %s", cache_key)


def _remove_expired_entries() -> None:
    """Clear expired values before adding new cache entries."""
    current_time = monotonic()
    expired_cache_keys = [
        cache_key
        for cache_key, cache_entry in _cache_entries.items()
        if cache_entry.expires_at <= current_time
    ]

    for cache_key in expired_cache_keys:
        del _cache_entries[cache_key]
        logger.info("Cache cleanup removed expired entry: %s", cache_key)
