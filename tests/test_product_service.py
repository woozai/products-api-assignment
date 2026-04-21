import pytest
import requests

from app.clients import dummyjson_client
from app.services import products as product_service
from app.services.products import ProductServiceError


class FakeResponse:
    """Small stand-in for a requests response object."""

    def __init__(self, payload, status_error=None):
        self.payload = payload
        self.status_error = status_error

    def raise_for_status(self):
        # This lets a test simulate non-2xx responses without real network calls.
        if self.status_error:
            raise self.status_error

    def json(self):
        return self.payload


def test_list_products_calls_dummyjson_with_pagination_params(monkeypatch):
    captured_request = {}

    def fake_get(url, params, timeout):
        # Capture the outgoing request so the test can inspect it later.
        captured_request["url"] = url
        captured_request["params"] = params
        captured_request["timeout"] = timeout
        return FakeResponse({"products": [], "total": 0, "skip": 10, "limit": 10})

    # Replace requests.get so this test stays fast and does not call DummyJSON.
    monkeypatch.setattr(dummyjson_client.requests, "get", fake_get)

    product_page = product_service.list_products(limit=10, skip=10)

    # The service should call the list endpoint with backend pagination params.
    assert captured_request["url"] == "https://dummyjson.com/products"
    assert captured_request["params"] == {"limit": 10, "skip": 10}
    assert captured_request["timeout"] == dummyjson_client.REQUEST_TIMEOUT_SECONDS
    assert product_page.total == 0


def test_search_products_calls_dummyjson_search_endpoint(monkeypatch):
    captured_request = {}

    def fake_get(url, params, timeout):
        # Capture the search request instead of sending it to the real API.
        captured_request["url"] = url
        captured_request["params"] = params
        captured_request["timeout"] = timeout
        return FakeResponse({"products": [], "total": 0, "skip": 0, "limit": 10})

    monkeypatch.setattr(dummyjson_client.requests, "get", fake_get)

    product_service.search_products(" phone ", limit=10, skip=0)

    # Search text is trimmed before it is sent as DummyJSON's q parameter.
    assert captured_request["url"] == "https://dummyjson.com/products/search"
    assert captured_request["params"] == {"q": "phone", "limit": 10, "skip": 0}
    assert captured_request["timeout"] == dummyjson_client.REQUEST_TIMEOUT_SECONDS


def test_product_normalization_uses_safe_fallbacks_for_missing_fields():
    # Products without a valid ID should be rejected instead of inventing one.
    with pytest.raises(product_service.ProductNormalizationError):
        product_service._normalize_product({})


def test_product_normalization_preserves_missing_numeric_values():
    # Missing numeric business fields should stay unknown instead of becoming zero.
    product = product_service._normalize_product({"id": 1})

    assert product.title == "Untitled product"
    assert product.description == "No description available."
    assert product.price is None
    assert product.rating is None
    assert product.stock is None
    assert product.brand == "N/A"
    assert product.category == "N/A"
    assert product.thumbnail == ""
    assert product.images == []


def test_product_normalization_filters_unsafe_image_urls():
    product = product_service._normalize_product(
        {
            "id": 1,
            "thumbnail": "javascript:alert(1)",
            "images": [
                "https://example.com/product.jpg",
                "data:text/html,<script>alert(1)</script>",
                "http://example.com/extra.jpg",
            ],
        }
    )

    assert product.thumbnail == ""
    assert product.images == [
        "https://example.com/product.jpg",
        "http://example.com/extra.jpg",
    ]


def test_service_raises_controlled_error_for_network_failure(monkeypatch):
    def fake_get(url, params, timeout):
        # Simulate a timeout from requests.
        assert url == "https://dummyjson.com/products"
        assert params == {"limit": 10, "skip": 0}
        assert timeout == dummyjson_client.REQUEST_TIMEOUT_SECONDS
        raise requests.Timeout("request timed out")

    monkeypatch.setattr(dummyjson_client.requests, "get", fake_get)

    # Routes catch ProductServiceError and show a friendly message to users.
    with pytest.raises(ProductServiceError):
        product_service.list_products(limit=10, skip=0)


def test_service_raises_controlled_error_for_bad_status(monkeypatch):
    def fake_get(url, params, timeout):
        # Simulate response.raise_for_status failing on a non-2xx response.
        assert url == "https://dummyjson.com/products"
        assert params == {"limit": 10, "skip": 0}
        assert timeout == dummyjson_client.REQUEST_TIMEOUT_SECONDS
        return FakeResponse({}, status_error=requests.HTTPError("server error"))

    monkeypatch.setattr(dummyjson_client.requests, "get", fake_get)

    with pytest.raises(ProductServiceError):
        product_service.list_products(limit=10, skip=0)


def test_service_raises_controlled_error_for_invalid_response_shape(monkeypatch):
    def fake_get(url, params, timeout):
        # Missing products list means the API response is not usable by the app.
        assert url == "https://dummyjson.com/products"
        assert params == {"limit": 10, "skip": 0}
        assert timeout == dummyjson_client.REQUEST_TIMEOUT_SECONDS
        return FakeResponse({"total": 1, "skip": 0, "limit": 10})

    monkeypatch.setattr(dummyjson_client.requests, "get", fake_get)

    with pytest.raises(ProductServiceError):
        product_service.list_products(limit=10, skip=0)


def test_service_skips_products_with_invalid_required_identity_fields(monkeypatch):
    def fake_get(url, params, timeout):
        assert url == "https://dummyjson.com/products"
        assert params == {"limit": 10, "skip": 0}
        assert timeout == dummyjson_client.REQUEST_TIMEOUT_SECONDS
        return FakeResponse(
            {
                "products": [
                    {"id": "bad", "title": "Broken"},
                    {"id": 2, "title": "Valid product"},
                ],
                "total": 2,
                "skip": 0,
                "limit": 10,
            }
        )

    monkeypatch.setattr(dummyjson_client.requests, "get", fake_get)

    product_page = product_service.list_products(limit=10, skip=0)

    assert [product.id for product in product_page.products] == [2]
