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

## How The App Works

The Flask route in `app/routes/products.py` reads the `page` and `q` query parameters from the browser URL.

- If `q` is empty, the backend calls the DummyJSON `/products` endpoint.
- If `q` has a search value, the backend calls the DummyJSON `/products/search` endpoint.
- Pagination is handled in the backend by converting the page number into DummyJSON `skip` and `limit` parameters.
- The service layer in `app/services/products.py` calls DummyJSON, validates the response, and normalizes product data before it reaches the template.
- The Jinja template renders the search form, product table, pagination links, empty states, and error messages.

## Gallery Behavior

Each product row has a `Gallery` button. The backend renders up to 3 image URLs into the button as HTML data attributes.

The JavaScript in `app/static/js/gallery.js` reads those rendered image URLs and inserts a gallery row directly below the clicked product row. It does not fetch product data from DummyJSON or any other API.

Clicking the same Gallery button closes the gallery. Opening another product gallery closes the previous one.

## Assumptions And Decisions

- Flask was chosen for the backend implementation.
- API calls, search, and pagination are handled in Python/Flask, not frontend JavaScript.
- The UI uses Jinja, plain CSS, and vanilla JavaScript only.
- The project uses `uv` for dependency management and local commands.
- Product data is not stored in a database; it is fetched from DummyJSON on request.
- Small dataclass models are used to keep product and pagination data predictable.
- The page size is fixed at 10 products per page.
- Tests are not included because they were not explicitly requested.

## Why These Choices

- Flask keeps the project small and clear while still supporting routes, templates, and backend service logic.
- Jinja is built into Flask, so it is a good fit for rendering the product table from backend data.
- Vanilla JavaScript is enough for the Gallery button behavior and follows the assignment requirement to avoid frontend frameworks.
- `uv` provides fast, reproducible dependency management through `pyproject.toml` and `uv.lock`.
- A service layer keeps DummyJSON API logic separate from routes and templates.
- Dataclass models make API data easier to pass around without adding database or schema complexity.
- Small utility functions keep pagination and type conversion reusable and easier to understand.

## Known Limitations

- The optional WordPress plugin bonus is not implemented.
- The app depends on DummyJSON being available at runtime.
- There is no local caching layer for product data.
- There is no custom favicon, so browsers may request `/favicon.ico` and receive a harmless 404.
