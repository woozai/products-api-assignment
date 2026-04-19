from abc import ABC, abstractmethod
from typing import Any


class CacheBackend(ABC):
    """Contract for cache backends used by product services."""

    @abstractmethod
    def get(self, cache_key: str) -> Any | None:
        """Return a cached value, or None when the key is missing or expired."""

    @abstractmethod
    def set(self, cache_key: str, value: Any, ttl_seconds: int) -> None:
        """Store a cached value for a limited time."""
