# Products API Assignment

Flask app for the DummyJSON products assignment. It renders a responsive product table with backend search, backend pagination, thumbnails, and a small vanilla JavaScript gallery.

Live demo: https://products-api-assignment-production.up.railway.app (available until May 21, 2026)

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

## Manual Run

If you prefer to run it without the helper scripts:

```bash
uv sync
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

Railway is configured to build from the root `Dockerfile` and run the app with Gunicorn in production.

## CI Security Scan

GitHub Actions scans the CI Docker image with Trivy and fails the build only for fixable `HIGH` or `CRITICAL` vulnerabilities.

## How The App Works

The browser sends `page` and `q` query parameters to the Flask route. The route calls a service layer that handles pagination, optional caching, and the DummyJSON request. The response is normalized into predictable models before Jinja renders the final HTML.

Products with invalid `id` values are skipped, and missing numeric fields such as price, rating, and stock are shown as `N/A` instead of fake zero values. The frontend JavaScript only enhances the gallery interaction and does not fetch product data.

## Backend Cache

Successful DummyJSON responses are cached in memory for 60 seconds per Flask process. Cache keys include the request mode, search query, page size, and skip value, so listing, search, and pagination states are cached separately.

Failed responses are not cached, the cache resets on restart, and it is intentionally local to a single process.

## Gallery Behavior
Each row has a Gallery button with up to 3 backend-rendered image URLs. Vanilla JavaScript opens the gallery below the selected row without making any browser-side API requests.


## Assumptions And Decisions

- The project uses `uv` for dependency management and local commands.
- API calls, search, and pagination stay in the backend, not frontend JavaScript.
- The UI uses Jinja, plain CSS, and vanilla JavaScript only.
- Product data is not stored in a database; successful API responses are cached briefly in memory.
- Products with invalid required identity data are skipped instead of being assigned fake fallback IDs.
- Missing numeric business values are displayed as `N/A` instead of `0`.

## Why These Choices

- Flask and Jinja keep the app small, readable, and close to the assignment requirements.
- A separate service layer keeps DummyJSON integration, normalization, and routes cleanly separated.
- Vanilla JavaScript is enough for the gallery behavior without adding unnecessary frontend complexity.
- The lightweight in-memory cache reduces repeated API calls without adding extra infrastructure for a small assignment.

## Known Limitations

- The optional WordPress plugin bonus is separate from the Flask app and must be installed in a WordPress site to run.
- The app depends on DummyJSON being available at runtime.
- The in-memory cache is local to one Flask process and is cleared on restart.

## WordPress Plugin Bonus

The WordPress plugin lives in:

```text
wordpress-plugin/products-assignment/
```

It is separate from the Flask app and must be run inside a WordPress site.

To test it locally, you need a working WordPress installation, for example a local site created with a desktop tool like Local, or any other WordPress environment.

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

The plugin renders the product table through PHP. DummyJSON requests, search, and pagination are handled on the WordPress backend. The gallery JavaScript only opens images that PHP already rendered into HTML data attributes.

Uninstall removes only the plugin-owned option. It does not delete the generated page or user-edited content.
