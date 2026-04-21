# Cache Planning Tasks

## Goal

Add simple backend caching for DummyJSON product responses so repeated page loads, searches, and pagination requests do not always call the external API.

Keep the cache small, understandable, and easy to remove or replace later. Do not add Redis, a database, Celery, or another service unless the project grows beyond the assignment needs.

## Recommended Approach

- [x] Use a small in-memory cache inside the Flask app process.
- [x] Cache only DummyJSON API responses after they are validated.
- [x] Use a short time-to-live, such as 60 seconds.
- [x] Build cache keys from the API mode, search query, page size, and skip value.
- [x] Keep cache logic separate from route functions.
- [x] Keep cache logic reusable for both product listing and product search.
- [x] Do not cache failed API responses.
- [x] Do not cache raw exceptions.
- [x] Do not cache user-specific data because this app does not have users or sessions.

## Suggested File Structure

- [x] Create `app/utils/cache.py`.
- [x] Keep the cache helper small and focused.
- [x] Use clear names such as `get_cached_value`, `set_cached_value`, and `build_products_cache_key`.
- [x] Use Python standard library tools only, such as `time.monotonic`.
- [x] Avoid adding a new dependency unless it provides clear value.

## Service Layer Integration

- [x] Add caching around successful DummyJSON calls in `app/services/products.py`.
- [x] Check the cache before calling DummyJSON.
- [x] Store the normalized or validated response shape after a successful API call.
- [x] Keep request timeout, status validation, and JSON validation in place.
- [x] Make sure search and normal listing use different cache keys.
- [x] Make sure different pages use different cache keys.
- [x] Make sure different search queries use different cache keys.

## Cache Behavior

- [x] Cache `/products?limit=10&skip=0` separately from `/products?limit=10&skip=10`.
- [x] Cache `/products/search?q=phone&limit=10&skip=0` separately from `/products/search?q=laptop&limit=10&skip=0`.
- [x] Trim search text before building the cache key.
- [x] Treat an empty search query as the normal product listing path.
- [x] Expire cached values after the selected TTL.
- [x] Remove expired values when they are read.
- [x] Keep memory use bounded with a simple maximum entry count if needed.

## Error Handling

- [x] If DummyJSON fails and there is no valid cached value, show the existing friendly error message.
- [x] Do not expose raw cache or API exceptions in the browser.
- [x] If cache code fails unexpectedly, prefer falling back to a live DummyJSON request.
- [x] Keep the current missing-field fallbacks unchanged.

## Documentation

- [x] Add a short README section explaining that API responses are cached briefly in memory.
- [x] Document the cache TTL.
- [x] Explain that the cache resets when the Flask process restarts.
- [x] Explain that this is intentionally simple and not shared across multiple server processes.

## Manual Verification

- [x] Start the app with `uv run flask --app run run`.
- [x] Open the product list page.
- [x] Refresh the same page and confirm it still loads.
- [x] Search for a product and refresh the same search URL.
- [x] Move between pagination pages and confirm each page still renders correctly.
- [x] Stop and restart the Flask app to confirm the cache can rebuild from empty state.

## Testing Notes

- [x] Do not add tests unless explicitly requested.
- [x] If tests are requested later, test cache key creation, TTL expiration, cache hit behavior, and cache miss behavior.
