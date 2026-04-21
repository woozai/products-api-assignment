# Products API Assignment

Flask web application for the DummyJSON products assignment. The app renders a product table with backend-powered search, backend pagination, thumbnail images, and a vanilla JavaScript image gallery.

Live demo: https://products-api-assignment-production.up.railway.app

## Prerequisites

- Python 3.13.12
- uv

## Quick Start For Reviewers

From the project root, run the script for your platform.

Windows:

```powershell
.\dev.ps1
```

or:

```bat
dev.bat
```

macOS or Linux:

```bash
./dev.sh
```

If needed, make the shell script executable once with `chmod +x dev.sh`.

These scripts install dependencies from `uv.lock` and start the app at `http://127.0.0.1:5000`.

## Installation

Install the project dependencies from the lockfile:

```bash
uv sync
```

## Run Locally

Start the Flask development server:

```bash
uv run flask --app run --debug run
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

## Railway Deployment

Railway deployment is configured in `railway.json` to build from the root `Dockerfile`.

The production container runs the app with Gunicorn, binds to Railway's injected `PORT` value, and avoids Flask's development server.

## CI Security Scan

GitHub Actions scans the CI Docker image with Trivy and fails the build only for fixable `HIGH` or `CRITICAL` vulnerabilities.

## How The App Works

The route reads `page` and `q` from the browser URL, then calls the service layer to either list products or search DummyJSON from the backend. Pagination is converted into DummyJSON `skip` and `limit` parameters, and the response is normalized before rendering.

Products with invalid `id` values are skipped, while missing numeric fields like price, rating, and stock are shown as `N/A` instead of fake zero values. The Jinja templates render the table, messages, and pagination links from that normalized data.

## Backend Cache

Successful DummyJSON responses are cached in memory for 60 seconds per Flask process. Cache keys include the request mode, search query, page size, and skip value, so listing, search, and pagination states are cached separately.

Failed responses are not cached, the cache resets on restart, and it is intentionally local to a single process.

## Code Structure

The app uses small abstract base classes for replaceable backend pieces. `MemoryCacheBackend` currently handles caching, but it follows a cache interface so it can later be replaced by Redis with less product-service code change.

`DummyJsonProductApiClient` currently handles product API calls, but it follows a product API client interface so another product API could be added later without changing routes or templates.

## Gallery Behavior

Each product row includes a `Gallery` button with up to 3 backend-rendered image URLs stored in data attributes. Vanilla JavaScript reads those values and inserts a gallery row directly below the clicked product without making any browser-side API requests.

Clicking the same button closes the gallery, and opening a different one closes the previous gallery first.

## Assumptions And Decisions

- Flask was chosen for the backend implementation.
- The project uses `uv` for dependency management and local commands.
- API calls, search, and pagination stay in the backend, not frontend JavaScript.
- The UI uses Jinja, plain CSS, and vanilla JavaScript only.
- Product data is not stored in a database; successful API responses are cached briefly in memory.
- The page size is fixed at 10 products per page.
- Products with invalid required identity data are skipped instead of being assigned fake fallback IDs.
- Missing numeric business values are displayed as `N/A` instead of `0`.
- Tests cover the main backend behavior and were added after being explicitly requested.

## Why These Choices

- Flask and Jinja keep the app small, readable, and close to the assignment requirements.
- A separate service layer keeps DummyJSON integration, normalization, and routes cleanly separated.
- Vanilla JavaScript is enough for the gallery behavior without adding unnecessary frontend complexity.
- `uv` and the Docker setup make local development, CI, and deployment consistent.
- The lightweight in-memory cache reduces repeated API calls without adding extra infrastructure for a small assignment.

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
