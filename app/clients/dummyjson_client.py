import logging
from typing import Any

import requests

from app.interfaces import ProductApiClient

DUMMYJSON_BASE_URL = "https://dummyjson.com"
REQUEST_TIMEOUT_SECONDS = 5

logger = logging.getLogger(__name__)


class ProductApiClientError(RuntimeError):
    """Raised when DummyJSON cannot return usable product data."""


class DummyJsonProductApiClient(ProductApiClient):
    """Product API client backed by DummyJSON."""

    def get_products(self, path: str, params: dict[str, Any]) -> dict[str, Any]:
        """Fetch a product response object from DummyJSON."""
        url = f"{DUMMYJSON_BASE_URL}{path}"

        try:
            # A timeout keeps the Flask request from hanging if the external API stalls.
            logger.info("Calling DummyJSON API: %s params=%s", url, params)
            response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT_SECONDS)
            # Turn 404/500/etc. into a controlled client error.
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as exc:
            raise ProductApiClientError("Could not fetch products from DummyJSON.") from exc
        except ValueError as exc:
            raise ProductApiClientError("DummyJSON returned invalid JSON.") from exc

        if not isinstance(data, dict):
            raise ProductApiClientError("DummyJSON response was not an object.")

        return data
