import pytest

from app.cache import MemoryCacheBackend
from app.utils import cache


@pytest.fixture(autouse=True)
def clear_cache_entries():
    """Start each cache test with an empty in-memory cache."""
    cache.default_cache_backend.clear()
    yield
    cache.default_cache_backend.clear()


def test_build_products_cache_key_normalizes_search_query():
    cache_key = cache.build_products_cache_key(
        "search",
        query=" Phone ",
        limit=10,
        skip=0,
    )

    # Search spacing and casing should not create separate cache entries.
    assert cache_key == "products:search:q=phone:limit=10:skip=0"


def test_cached_value_can_be_read_before_it_expires():
    product_page = {"products": [], "total": 0}

    cache.set_cached_value("products:list:q=:limit=10:skip=0", product_page)

    # A fresh cache entry should be returned without changing its shape.
    assert cache.get_cached_value("products:list:q=:limit=10:skip=0") == product_page


def test_expired_cached_value_is_removed():
    cache_key = "products:list:q=:limit=10:skip=0"

    cache.set_cached_value(cache_key, {"products": []}, ttl_seconds=0)

    # Expired entries should behave like a cache miss and be deleted.
    assert cache.get_cached_value(cache_key) is None
    assert not cache.default_cache_backend.has_key(cache_key)


def test_memory_cache_backend_removes_oldest_entry_when_full():
    cache_backend = MemoryCacheBackend(max_entries=1)

    cache_backend.set("first", "old")
    cache_backend.set("second", "new")

    # The backend keeps memory bounded by removing the oldest stored key.
    assert cache_backend.get("first") is None
    assert cache_backend.get("second") == "new"
