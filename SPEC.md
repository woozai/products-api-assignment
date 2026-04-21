# Flask Products Assignment Specification

## 1. Project Summary

This project is a Flask web application that renders a dynamic products table using data from the DummyJSON Products API.

The application includes backend-driven data retrieval, backend search, backend pagination, friendly error handling, short-lived in-memory caching, and a small vanilla JavaScript gallery interaction for product images.

A separate optional WordPress plugin bonus implementation also exists under `wordpress-plugin/products-assignment/`.

## 2. Current Technology Decisions

- Backend: Python 3.13 with Flask.
- Templates: Jinja.
- Frontend behavior: vanilla JavaScript only.
- Styling: plain CSS split into focused component files.
- Package management: `uv`.
- External API: DummyJSON Products API.
- HTTP client: `requests`.
- Tests: `pytest`.
- Type checks: `mypy` for the Flask `app/` package.
- Container support: Docker.
- CI: GitHub Actions runs dependency install, tests, type checks, Flask route smoke check, Docker build, Trivy image scan, and Docker smoke check.

## 3. Implemented Assignment Requirements

### Backend Features

- Fetch products from DummyJSON in the Flask backend.
- Render a dynamic products table with Jinja.
- Implement search through the DummyJSON `/products/search` endpoint.
- Implement pagination in the backend using DummyJSON `limit` and `skip` parameters.
- Validate user-controlled query parameters such as `page` and `q`.
- Handle API errors, empty results, invalid page values, bad API shapes, invalid JSON, and missing product fields gracefully.
- Normalize raw product dictionaries into dataclass models before rendering.
- Cache successful product responses briefly in memory.

### Required Table Columns

The products table includes:

- Title
- Description
- Price
- Rating
- Stock
- Brand
- Category
- Thumbnail as an image or a fallback label
- Gallery button

### JavaScript Feature

Each product row includes a Gallery button.

When clicked:

- A gallery row opens directly between the clicked product row and the next product row.
- The gallery displays up to 3 product images.
- If fewer than 3 images exist, the available images are displayed.
- If no images exist, a friendly fallback message is displayed.
- Opening another product gallery closes the previous one.
- Clicking the same Gallery button closes the open gallery.
- The browser does not fetch product data from DummyJSON.

### Documentation

`README.md` includes:

- Prerequisites.
- Installation instructions.
- Local run instructions.
- Test instructions.
- Docker instructions.
- CI security scan explanation.
- App behavior explanation.
- Cache behavior.
- Important decisions.
- Known limitations.
- WordPress plugin bonus instructions.

## 4. Non-Goals

- Do not use frontend frameworks.
- Do not implement product search in frontend JavaScript.
- Do not implement pagination in frontend JavaScript.
- Do not fetch all products and slice locally when DummyJSON supports `limit` and `skip`.
- Do not store products in a database for the Flask app.
- Do not mix the WordPress plugin implementation into the Flask app.

## 5. Current Project Structure

```text
.
|-- .github/
|   `-- workflows/
|       `-- ci.yml
|-- app/
|   |-- __init__.py
|   |-- cache/
|   |   |-- __init__.py
|   |   `-- memory_cache.py
|   |-- clients/
|   |   |-- __init__.py
|   |   `-- dummyjson_client.py
|   |-- interfaces/
|   |   |-- __init__.py
|   |   |-- cache_backend.py
|   |   `-- product_api_client.py
|   |-- models/
|   |   |-- __init__.py
|   |   |-- pagination.py
|   |   |-- product.py
|   |   `-- product_page.py
|   |-- routes/
|   |   |-- __init__.py
|   |   `-- products.py
|   |-- services/
|   |   |-- __init__.py
|   |   `-- products.py
|   |-- static/
|   |   |-- css/
|   |   |   |-- styles.css
|   |   |   `-- components/
|   |   `-- js/
|   |       `-- gallery.js
|   |-- templates/
|   |   |-- base.html
|   |   |-- index.html
|   |   `-- components/
|   `-- utils/
|       |-- __init__.py
|       |-- cache.py
|       |-- pagination.py
|       `-- type_casting.py
|-- tests/
|   |-- conftest.py
|   |-- test_cache_utils.py
|   |-- test_pagination_utils.py
|   |-- test_product_service.py
|   `-- test_products_route.py
|-- wordpress-plugin/
|   `-- products-assignment/
|-- CODE_STUDY_ROADMAP.md
|-- Dockerfile
|-- README.md
|-- SPEC.md
|-- pyproject.toml
|-- run.py
`-- uv.lock
```

## 6. Backend Design

### Flask App Factory

`app/__init__.py` exposes `create_app()`.

The app factory:

- Configures basic logging.
- Creates the Flask app.
- Registers the products blueprint.
- Returns the app.

`run.py` imports `create_app()` and exposes the Flask app as `app` for local `flask --app run` commands and Docker.

### Flask Route Layer

The main route lives in `app/routes/products.py` and handles `GET /`.

The route:

- Reads `page` and `q` from `request.args`.
- Normalizes invalid or missing page values.
- Trims the search query.
- Converts the 1-based page number into DummyJSON's `skip` value.
- Calls `search_products()` when `q` is non-empty.
- Calls `list_products()` when `q` is empty.
- Catches `ProductServiceError` and renders a friendly error message.
- Builds pagination data for the template.
- Redirects out-of-range page requests to the last valid page when products exist.
- Passes products, pagination data, query text, and error/empty state values to Jinja.

Route modules live in `app/routes/` and are registered from `app/__init__.py` using Flask blueprints.

### Product Service Layer

The product service lives in `app/services/products.py`.

The service:

- Calls `/products` for normal listing.
- Calls `/products/search` for non-empty search queries.
- Sends `limit`, `skip`, and `q` as structured request parameters.
- Builds stable cache keys for list and search requests.
- Reads and writes successful `ProductPage` responses from/to cache.
- Validates that the API response includes a `products` list.
- Normalizes product dictionaries for template use.
- Converts lower-level API client failures into `ProductServiceError`.
- Continues without caching if cache read or write fails.

### DummyJSON Client Layer

The DummyJSON client lives in `app/clients/dummyjson_client.py`.

The client:

- Owns the DummyJSON base URL.
- Builds the full request URL.
- Uses `requests.get()` with structured query parameters.
- Uses a 5-second timeout.
- Calls `raise_for_status()` for non-2xx responses.
- Parses JSON.
- Verifies the response is a JSON object.
- Raises `ProductApiClientError` for network errors, HTTP errors, invalid JSON, or unexpected response shape.

### Interfaces

Interfaces live in `app/interfaces/`.

- `ProductApiClient` defines the contract for product API clients.
- `CacheBackend` defines the contract for cache implementations.

The current service uses:

- `DummyJsonProductApiClient`
- `MemoryCacheBackend`

These interfaces keep the service testable and make future replacements, such as another API client or Redis cache, easier.

## 7. Data Models And Normalization

Normalized data shapes live in `app/models/`.

- `Product` represents one normalized product.
- `ProductPage` represents a normalized page of products returned by DummyJSON.
- `Pagination` represents the pagination state needed by the UI.

Type conversion and field cleanup live in `app/utils/type_casting.py`.

Normalization handles:

- Missing or invalid product dictionaries.
- Missing titles.
- Missing descriptions.
- Invalid prices, ratings, stock values, IDs, totals, limits, and skips.
- Missing brands or categories.
- Missing thumbnails.
- Unsafe image URLs.
- Invalid image lists.

Only `http` and `https` image URLs are rendered.

## 8. Pagination

Pagination logic lives in `app/utils/pagination.py`.

Pagination:

- Uses 1-based page numbers in URLs.
- Uses a fixed page size of 10 products per page.
- Calculates `skip` as `(page - 1) * limit`.
- Calculates total pages from DummyJSON `total`.
- Returns at least 1 total page so empty states render cleanly.
- Preserves the active search query in pagination links.
- Uses `None` for unavailable previous or next links.

The pagination component lives in `app/templates/components/pagination.html`.

## 9. Search

Search is backend-driven.

The search form lives in `app/templates/components/search_form.html`.

Search behavior:

- The form submits with `method="get"`.
- The search input uses the `q` query parameter.
- The route trims the query.
- Empty query values use the normal `/products` endpoint.
- Non-empty query values use `/products/search`.
- Pagination links preserve the current `q` value.
- Empty search results display a friendly empty-state message instead of an error.

## 10. Cache

Caching is implemented in `app/cache/memory_cache.py`.

Cache behavior:

- Successful product responses are cached for 60 seconds.
- The cache stores values inside the running Flask process.
- Cache keys include request mode, normalized search query, limit, and skip.
- Expired entries are removed.
- If the cache reaches its maximum size, the oldest entry is removed.
- Cache read or write failures are logged but do not break product loading.

Known cache limitations:

- It resets when Flask restarts.
- It is not shared across multiple processes or containers.
- It is not intended as a production distributed cache.

## 11. Frontend Design

### Jinja Templates

Templates live in `app/templates/`.

`base.html`:

- Defines the page shell.
- Loads the main stylesheet.
- Loads `gallery.js` with `defer`.

`index.html`:

- Extends `base.html`.
- Includes smaller template components.

Component templates render:

- Page header.
- Error and empty messages.
- Search form.
- Result status.
- Pagination controls.
- Product table.
- Product rows.

Product image data for the gallery is rendered into each Gallery button using a safe JSON value in a `data-product-images` attribute.

### Gallery JavaScript

Gallery behavior lives in `app/static/js/gallery.js`.

JavaScript:

- Attaches event listeners after `DOMContentLoaded`.
- Reads image URLs from `data-product-images`.
- Parses the image list safely.
- Inserts or removes a gallery row directly after the clicked product row.
- Renders up to 3 image elements with useful `alt` text.
- Shows a fallback message when no gallery images are available.
- Updates `aria-expanded` and `aria-label`.
- Avoids API calls and frontend frameworks.

### CSS

CSS lives in `app/static/css/`.

`styles.css` imports focused component styles:

- Base styles.
- Layout styles.
- Form styles.
- Message styles.
- Table styles.
- Gallery styles.
- Pagination styles.
- Responsive styles.

## 12. Error Handling

The app handles:

- Invalid page values.
- Out-of-range page values.
- Empty search results.
- DummyJSON timeouts or unavailable API.
- Non-2xx API responses.
- Invalid JSON responses.
- Unexpected API response shapes.
- Missing product fields.
- Missing or unsafe image data.
- Cache read or write failures.

Users see friendly messages. Raw exception details are logged and are not shown in the browser.

## 13. Testing Strategy

Automated backend tests exist under `tests/`.

The tests cover:

- Pagination utility behavior.
- Cache utility behavior.
- Product service behavior.
- Product route behavior.
- Error handling paths.
- Product normalization behavior.

Tests should avoid depending on the real DummyJSON network service. Use fakes or monkeypatching when checking service and route behavior.

Run tests with:

```bash
uv run pytest
```

## 14. CI/CD Specification

GitHub Actions workflow lives in `.github/workflows/ci.yml`.

The CI workflow runs on pushes and pull requests.

Current CI stages:

- Check out repository.
- Install Python 3.13.
- Install `uv`.
- Run `uv sync --locked`.
- Run backend tests with `uv run pytest`.
- Run type checks with `uv run mypy app`.
- Smoke check Flask routes with `uv run flask --app run routes`.
- Build Docker image as `products-api-assignment:ci`.
- Scan the Docker image with Trivy.
- Run the Docker container on port 8000.
- Smoke check the running container with `curl`.
- Stop the Docker container.

Trivy scans:

- OS packages.
- Python library packages.
- `HIGH` and `CRITICAL` vulnerabilities.

CI fails on actionable high or critical vulnerabilities with fixed versions available.

Deployment is not configured. Add deployment only after a target host is chosen, and store any secrets in GitHub Actions secrets instead of the repo.

## 15. Docker Specification

The Dockerfile:

- Uses `python:3.13-slim`.
- Copies `uv` from the official Astral image.
- Installs dependencies from `pyproject.toml` and `uv.lock`.
- Copies the Flask app and `run.py`.
- Exposes port 8000.
- Runs Flask with `uv run flask --app run run --host 0.0.0.0 --port 8000`.

Build locally with:

```bash
docker build -t products-api-assignment .
```

Run locally with:

```bash
docker run --rm -p 8000:8000 products-api-assignment
```

## 16. WordPress Plugin Bonus

The WordPress plugin bonus is implemented separately from the Flask app.

Location:

```text
wordpress-plugin/products-assignment/
```

The plugin:

- Registers and enqueues its own assets.
- Fetches products from DummyJSON on the WordPress backend.
- Supports backend search and pagination.
- Renders the product table through PHP templates.
- Adds a shortcode: `[products_assignment]`.
- Creates or reuses a page titled `Compare Assignment` on activation.
- Uses vanilla JavaScript for the gallery interaction.
- Keeps plugin code separate from the Flask implementation.

Uninstall removes the plugin-owned option. It does not delete generated pages or user-edited content.

## 17. Known Limitations

- The Flask app depends on DummyJSON availability at runtime when a cache entry is not available.
- The in-memory cache is local to one Flask process and is cleared on restart.
- The in-memory cache is not shared across multiple workers, processes, or containers.
- The Docker container runs Flask directly, which is acceptable for this assignment but not a full production WSGI deployment.
- There is no custom favicon, so browsers may request `/favicon.ico` and receive a harmless 404.
- The WordPress plugin must be installed in a WordPress site to run.

## 18. Future Improvement Ideas

- Add configurable API base URL, timeout, page size, and cache TTL.
- Replace the in-memory cache with Redis for production.
- Add product sorting.
- Add more detailed observability around API latency and cache hit rate.
- Add stricter response validation if the API contract grows.
- Use a production WSGI server for deployment.
