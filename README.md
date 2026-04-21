# Products API Assignment

Flask web application for the DummyJSON products assignment. The app renders a product table with backend-powered search, backend pagination, thumbnail images, and a vanilla JavaScript image gallery.

## Prerequisites

- Python 3.13.12
- uv

## Installation

Install the project dependencies from the lockfile:

```bash
uv sync
```

## Run Locally

Start the Flask development server:

```bash
uv run flask --app run run
```

Open the local URL printed in the terminal, usually:

```text
http://127.0.0.1:5000
```

## Run Tests

Run the backend test suite:

```bash
uv run pytest
```

## Docker

Build the container image:

```bash
docker build -t products-api-assignment .
```

Run the container:

```bash
docker run --rm -p 8000:8000 products-api-assignment
```

Then open:

```text
http://127.0.0.1:8000
```

## CI Security Scan

GitHub Actions builds the Docker image with the local CI tag:

```text
products-api-assignment:ci
```

The workflow scans that image with Trivy before running the container smoke check. The image is scanned only inside CI and is not pushed to a registry.

Trivy checks:

- operating system packages from the Docker base image, such as Debian packages;
- Python packages installed in the container;
- only vulnerability findings, not secrets or configuration issues;
- only `HIGH` and `CRITICAL` severities.

CI fails when Trivy finds a `HIGH` or `CRITICAL` vulnerability that has a fixed version available. Unfixed vulnerabilities are still printed in the CI logs, but they do not fail the build because there is no patched package version to upgrade to yet.

## How The App Works

The Flask route in `app/routes/products.py` reads the `page` and `q` query parameters from the browser URL.

- If `q` is empty, the backend calls the DummyJSON `/products` endpoint.
- If `q` has a search value, the backend calls the DummyJSON `/products/search` endpoint.
- Pagination is handled in the backend by converting the page number into DummyJSON `skip` and `limit` parameters.
- The service layer in `app/services/products.py` calls DummyJSON, validates the response, and normalizes product data before it reaches the template.
- Products missing a valid `id` are skipped during normalization instead of being assigned a fake fallback ID.
- Missing or invalid numeric business fields like price, rating, and stock are rendered as `N/A` instead of `0`.
- Successful product responses are cached briefly in memory so repeated requests do not always call DummyJSON.
- The Jinja template renders the search form, product table, pagination links, empty states, and error messages.

## Backend Cache

The app uses a small in-memory cache for successful DummyJSON product responses. Cached values are stored inside the running Flask process for 60 seconds.

Cache keys include the request type, search query, page size, and skip value. That means normal listing pages, search results, and different pagination pages are cached separately.

The cache is intentionally simple:

- failed API responses are not cached;
- raw exceptions are not cached;
- the cache resets when Flask restarts;
- the cache is not shared across multiple server processes or containers.

## Code Structure

The app uses small abstract base classes for replaceable backend pieces. `MemoryCacheBackend` currently handles caching, but it follows a cache interface so it can later be replaced by Redis with less product-service code change.

`DummyJsonProductApiClient` currently handles product API calls, but it follows a product API client interface so another product API could be added later without changing routes or templates.

## Gallery Behavior

Each product row has a `Gallery` button. The backend renders up to 3 image URLs into the button as HTML data attributes.

The JavaScript in `app/static/js/gallery.js` reads those rendered image URLs and inserts a gallery row directly below the clicked product row. It does not fetch product data from DummyJSON or any other API.

Clicking the same Gallery button closes the gallery. Opening another product gallery closes the previous one.

## Assumptions And Decisions

- Flask was chosen for the backend implementation.
- API calls, search, and pagination are handled in Python/Flask, not frontend JavaScript.
- The UI uses Jinja, plain CSS, and vanilla JavaScript only.
- The project uses `uv` for dependency management and local commands.
- Product data is not stored in a database; successful API responses are cached briefly in memory.
- Small dataclass models are used to keep product and pagination data predictable.
- The page size is fixed at 10 products per page.
- Tests cover the main backend behavior and were added after being explicitly requested.

## Why These Choices

- Flask keeps the project small and clear while still supporting routes, templates, and backend service logic.
- Jinja is built into Flask, so it is a good fit for rendering the product table from backend data.
- Vanilla JavaScript is enough for the Gallery button behavior and follows the assignment requirement to avoid frontend frameworks.
- `uv` provides fast, reproducible dependency management through `pyproject.toml` and `uv.lock`.
- A service layer keeps DummyJSON API logic separate from routes and templates.
- Dataclass models make API data easier to pass around without adding database or schema complexity.
- Small utility functions keep pagination and type conversion reusable and easier to understand.
- A small in-memory cache reduces repeated external API calls without adding Redis or another service for this assignment.
- Abstract base classes keep the cache and product API client replaceable without adding a heavy framework.

## Known Limitations

- The optional WordPress plugin bonus is separate from the Flask app and must be installed in a WordPress site to run.
- The app depends on DummyJSON being available at runtime.
- The in-memory cache is local to one Flask process and is cleared on restart.
- There is no custom favicon, so browsers may request `/favicon.ico` and receive a harmless 404.

## WordPress Plugin Bonus

The optional WordPress plugin lives in:

```text
wordpress-plugin/products-assignment/
```

It is separate from the Flask app and must be run inside a WordPress site.

To run it locally:

1. Copy or symlink `wordpress-plugin/products-assignment/` into a WordPress plugins folder:

```text
wp-content/plugins/products-assignment/
```

2. In WordPress admin, activate:

```text
Products Assignment
```

3. Open the generated page:

```text
Compare Assignment
```

The plugin creates or reuses that page on activation and inserts:

```text
[products_assignment]
```

You can also place `[products_assignment]` on any other page.

The plugin renders the product table through PHP. DummyJSON requests, search, and pagination are handled on the WordPress backend. The gallery JavaScript only opens images that PHP already rendered into HTML data attributes.

Uninstall removes only the plugin-owned option. It does not delete the generated page or user-edited content.
