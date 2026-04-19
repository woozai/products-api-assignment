import logging
from dataclasses import dataclass
from time import monotonic
from typing import Any

from app.interfaces import CacheBackend

CACHE_TTL_SECONDS = 60
MAX_CACHE_ENTRIES = 128

logger = logging.getLogger(__name__)


@dataclass
class CacheEntry:
    """Value stored in the in-memory cache with its expiration time."""

    value: Any
    expires_at: float


class MemoryCacheBackend(CacheBackend):
    """Small in-memory cache backend for the Flask process."""

    def __init__(self, max_entries: int = MAX_CACHE_ENTRIES) -> None:
        self.max_entries = max_entries
        self._cache_entries: dict[str, CacheEntry] = {}

    def get(self, cache_key: str) -> Any | None:
        """Return a cached value when it exists and has not expired."""
        cache_entry = self._cache_entries.get(cache_key)

        if cache_entry is None:
            logger.info("Cache miss: %s", cache_key)
            return None

        if cache_entry.expires_at <= monotonic():
            del self._cache_entries[cache_key]
            logger.info("Cache expired: %s", cache_key)
            return None

        logger.info("Cache hit: %s", cache_key)
        return cache_entry.value

    def set(self, cache_key: str, value: Any, ttl_seconds: int = CACHE_TTL_SECONDS) -> None:
        """Store a value in memory for a short time."""
        self._remove_expired_entries()

        if cache_key not in self._cache_entries and len(self._cache_entries) >= self.max_entries:
            oldest_cache_key = next(iter(self._cache_entries))
            del self._cache_entries[oldest_cache_key]
            logger.info("Cache full, removed oldest entry: %s", oldest_cache_key)

        self._cache_entries[cache_key] = CacheEntry(
            value=value,
            expires_at=monotonic() + ttl_seconds,
        )
        logger.info("Cache stored: %s", cache_key)

    def clear(self) -> None:
        """Clear all cached values for tests or local debugging."""
        self._cache_entries.clear()

    def has_key(self, cache_key: str) -> bool:
        """Return True when a raw cache entry currently exists."""
        return cache_key in self._cache_entries

    def _remove_expired_entries(self) -> None:
        """Clear expired values before adding new cache entries."""
        current_time = monotonic()
        expired_cache_keys = [
            cache_key
            for cache_key, cache_entry in self._cache_entries.items()
            if cache_entry.expires_at <= current_time
        ]

        for cache_key in expired_cache_keys:
            del self._cache_entries[cache_key]
            logger.info("Cache cleanup removed expired entry: %s", cache_key)
