from abc import ABC, abstractmethod
from typing import Any


class ProductApiClient(ABC):
    """Contract for clients that fetch product data from an external API."""

    @abstractmethod
    def get_products(self, path: str, params: dict[str, Any]) -> dict[str, Any]:
        """Fetch product data for a path and request parameters."""
