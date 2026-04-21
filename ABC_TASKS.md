# ABC Refactor Tasks

## Goal

Use Python abstract base classes to make the cache backend and product API client replaceable while keeping the assignment simple and readable.

Do not add Redis, a database, a dependency injection framework, or any new package.

## Interfaces

- [x] Create `app/interfaces/`.
- [x] Create `app/interfaces/__init__.py`.
- [x] Create `app/interfaces/cache_backend.py`.
- [x] Define `CacheBackend` with `get` and `set`.
- [x] Create `app/interfaces/product_api_client.py`.
- [x] Define `ProductApiClient` with `get_products`.
- [x] Keep interface names clear and purpose-based.

## Cache Backend

- [x] Create `app/cache/`.
- [x] Create `app/cache/__init__.py`.
- [x] Create `app/cache/memory_cache.py`.
- [x] Move in-memory cache storage into `MemoryCacheBackend`.
- [x] Keep `build_products_cache_key` available from `app/utils/cache.py`.
- [x] Remove temporary cache wrapper functions from `app/utils/cache.py` after `app/services/products.py` uses `MemoryCacheBackend` directly.
- [x] Keep 60-second default TTL.
- [x] Keep max cache entries at 128.
- [x] Keep cache hit, miss, store, expired, and cleanup logs.
- [x] Keep expired entries removed when read.
- [x] Keep memory bounded by removing the oldest entry when full.
- [x] Keep only successful normalized `ProductPage` values cached by the product service.
- [x] Do not cache failed API responses, invalid API shapes, or raw exceptions.
- [x] Keep cache failures non-fatal to product loading.
- [x] Keep a simple way to clear the in-memory cache for tests.

## Product API Client

- [x] Create `app/clients/`.
- [x] Create `app/clients/__init__.py`.
- [x] Create `app/clients/dummyjson_client.py`.
- [x] Move DummyJSON base URL into the DummyJSON client.
- [x] Move request timeout into the DummyJSON client.
- [x] Move `requests.get` call into the DummyJSON client.
- [x] Keep request params structured with `params`.
- [x] Keep timeout handling.
- [x] Keep non-2xx response handling.
- [x] Keep invalid JSON handling.
- [x] Keep raw API response validation.
- [x] Keep DummyJSON API call logging.
- [x] Convert client failures into the existing friendly product service error flow.
- [x] Avoid circular imports between the API client and product service.

## Product Service Integration

- [x] Update `app/services/products.py` to use `CacheBackend`.
- [x] Update `app/services/products.py` to use `ProductApiClient`.
- [x] Keep `list_products(limit, skip)` public behavior unchanged.
- [x] Keep `search_products(query, limit, skip)` public behavior unchanged.
- [x] Keep product normalization in the service layer.
- [x] Keep all product field fallbacks unchanged.
- [x] Keep safe image URL filtering unchanged.
- [x] Keep `ProductServiceError` as the route-facing service error.
- [x] Keep cache key behavior unchanged.
- [x] Keep search and listing cache keys separate.
- [x] Keep different pages cached separately.
- [x] Keep different search queries cached separately.
- [x] Keep friendly error behavior unchanged.
- [x] Keep routes, templates, pagination helpers, and gallery JavaScript behavior unchanged.

## Documentation

- [x] Update README with a short note explaining the ABC refactor.
- [x] Explain that `MemoryCacheBackend` can later be replaced by Redis.
- [x] Explain that `DummyJsonProductApiClient` can later be replaced by another product API client.
- [x] Keep the explanation short and beginner-friendly.

## Verification

- [x] Run `uv run pytest`.
- [x] Run `uv run mypy app`.
- [x] Update existing tests to use the new concrete cache/client locations.
- [x] Do not remove existing backend behavior coverage.
- [x] Start the app with `uv run flask --app run run`.
- [x] Open the product list page.
- [x] Confirm first request logs a cache miss and DummyJSON call.
- [x] Refresh within 60 seconds and confirm cache hit.
- [x] Search for a product and confirm search still works.
- [x] Paginate and confirm pagination still works.
- [x] Confirm gallery behavior is unchanged.

## Testing Notes

- [x] Do not add new tests unless explicitly requested.
- [x] If tests are requested, cover `MemoryCacheBackend`, `DummyJsonProductApiClient`, and product service integration with fake implementations.
