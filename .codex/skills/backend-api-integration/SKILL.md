---
name: backend-api-integration
description: Use when fetching product data from DummyJSON in the Flask backend, transforming product API responses, handling `limit` and `skip`, or creating service-layer functions for product listing and search. Do not use for browser-side fetching; the assignment requires backend API calls.
---

# Backend API Integration

## Purpose

Keep external API access in the backend service layer so routes and templates receive clean, predictable data.

## Responsibilities

- Store the external API base URL in one obvious place.
- Build API URLs and query parameters with a structured request API.
- Send backend HTTP requests from a service/helper module.
- Parse JSON responses and validate the fields the app depends on.
- Normalize API data into simple dictionaries for templates.
- Return enough metadata for pagination, such as total count, limit, and skip.
- Provide all fields required by the assignment table: title, description, price, rating, stock, brand, category, thumbnail, and images for the gallery.
- Reuse one internal request helper for shared API behavior such as timeout, status checking, and JSON parsing.
- Keep product normalization in one reusable function.
- Use purpose-revealing service names such as `list_products`, `search_products`, `_fetch_products`, and `_normalize_product`.

## Rules

- Prefer `requests.get(..., params={...}, timeout=...)` or the project's existing HTTP helper.
- Always use a timeout for external API calls.
- Keep API-specific field names inside the service layer when practical.
- Do not hardcode sample API responses into application logic.
- Do not fetch the full dataset just to paginate or search locally when the API supports `limit`, `skip`, or search endpoints.
- Keep the browser free of product API calls unless a later requirement explicitly changes that.
- Do not duplicate request, error handling, or normalization logic between list and search functions.
- Do not use generic service names like `get_data`, `call_api`, or `process` when a specific product/API purpose is known.
- Pair with `error-handling` for network failures, bad status codes, invalid JSON, and missing fields.
- Pair with `code-commenting` when response transformation is not immediately obvious.

## DummyJSON Notes

- Product listing usually uses `/products` with `limit` and `skip`.
- Product search usually uses `/products/search` with `q`, `limit`, and `skip`.
- Product responses commonly include `products`, `total`, `skip`, and `limit`.
- Product image data can come from `thumbnail` and `images`.

## Before Finishing

- Confirm API calls happen in backend Python code, not templates.
- Confirm the service returns a stable shape even when no products are found.
- Confirm failures are converted into user-friendly app behavior.
- Confirm each product has safe fallback values for optional or missing fields.
- Confirm shared API behavior lives in reusable helpers.
