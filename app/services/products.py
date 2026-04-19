import logging
from typing import Any

import requests

from app.models import Product, ProductPage
from app.utils.cache import build_products_cache_key, get_cached_value, set_cached_value
from app.utils.type_casting import (
    to_float,
    to_int,
    to_safe_image_url,
    to_safe_image_urls,
    to_str,
)

# Keep the external API details in this service so routes and templates stay simple.
DUMMYJSON_BASE_URL = "https://dummyjson.com"
REQUEST_TIMEOUT_SECONDS = 5

logger = logging.getLogger(__name__)


class ProductServiceError(RuntimeError):
    """Raised when DummyJSON cannot return usable product data."""


def list_products(limit: int, skip: int = 0) -> ProductPage:
    """Fetch a page of products from DummyJSON."""
    return _fetch_products("/products", {"limit": limit, "skip": skip})


def search_products(query: str, limit: int, skip: int = 0) -> ProductPage:
    """Search products through DummyJSON using backend request parameters."""
    # DummyJSON uses q for search text, plus the same pagination params as listing.
    params = {"q": query.strip(), "limit": limit, "skip": skip}
    return _fetch_products("/products/search", params)


def _fetch_products(path: str, params: dict[str, Any]) -> ProductPage:
    api_mode = "search" if path.endswith("/search") else "list"
    cache_key = build_products_cache_key(
        api_mode,
        query=to_str(params.get("q"), ""),
        limit=to_int(params.get("limit")),
        skip=to_int(params.get("skip")),
    )
    try:
        cached_product_page = get_cached_value(cache_key)
    except Exception:
        logger.warning("Cache read failed, falling back to DummyJSON.", exc_info=True)
        cached_product_page = None

    if isinstance(cached_product_page, ProductPage):
        return cached_product_page

    # Both list and search responses should have products, total, skip, and limit.
    data = _get_json(path, params)
    products_data = data.get("products")

    if not isinstance(products_data, list):
        raise ProductServiceError("DummyJSON response did not include a products list.")

    # Convert the API response into a stable shape for routes and templates.
    product_page = ProductPage(
        products=[_normalize_product(item) for item in products_data],
        total=to_int(data.get("total")),
        skip=to_int(data.get("skip")),
        limit=to_int(data.get("limit")),
    )
    try:
        set_cached_value(cache_key, product_page)
    except Exception:
        logger.warning("Cache write failed, continuing without caching this response.", exc_info=True)

    return product_page


def _get_json(path: str, params: dict[str, Any]) -> dict[str, Any]:
    url = f"{DUMMYJSON_BASE_URL}{path}"

    try:
        # A timeout keeps the Flask request from hanging if the external API stalls.
        logger.info("Calling DummyJSON API: %s params=%s", url, params)
        response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT_SECONDS)
        # Turn 404/500/etc. into a controlled ProductServiceError.
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as exc:
        raise ProductServiceError("Could not fetch products from DummyJSON.") from exc
    except ValueError as exc:
        raise ProductServiceError("DummyJSON returned invalid JSON.") from exc

    if not isinstance(data, dict):
        raise ProductServiceError("DummyJSON response was not an object.")

    return data


def _normalize_product(data: Any) -> Product:
    # If DummyJSON returns a broken product item, keep rendering with safe defaults.
    if not isinstance(data, dict):
        data = {}

    # Normalize every field used by the table or gallery.
    return Product(
        id=to_int(data.get("id")),
        title=to_str(data.get("title"), "Untitled product"),
        description=to_str(data.get("description"), "No description available."),
        price=to_float(data.get("price")),
        rating=to_float(data.get("rating")),
        stock=to_int(data.get("stock")),
        brand=to_str(data.get("brand")),
        category=to_str(data.get("category")),
        thumbnail=to_safe_image_url(data.get("thumbnail")),
        images=to_safe_image_urls(data.get("images")),
    )
