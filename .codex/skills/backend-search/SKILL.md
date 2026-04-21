---
name: backend-search
description: Use when implementing or changing backend product search for the DummyJSON products assignment, including search query handling, `/products/search` API calls, search URLs, empty search states, or combining search with pagination. Do not use for local browser filtering; the assignment requires backend search.
---

# Backend Search

## Purpose

Run product search through the backend and external API so search results, pagination, and templates stay consistent.

## Responsibilities

- Read the search query from request parameters, usually `q`.
- Trim whitespace and handle an empty query clearly.
- Call the external search endpoint when a query exists.
- Fall back to the normal product listing when no query exists, unless the app intentionally shows an empty search state.
- Preserve the active query across pagination links.
- Return clean results and metadata to the template.
- Dynamically render the table with only products matching the user's search query.
- Share list and search flow where practical so only the endpoint/query details differ.
- Use names that make search behavior obvious, such as `search_query`, `search_products`, and `has_search_query`.

## Rules

- Do not filter products in frontend JavaScript when the backend/API should search.
- Do not fetch all products just to perform local search.
- Do not update search results only in the browser.
- Do not duplicate product normalization or pagination logic for search results.
- Do not use unclear names like `term`, `text`, or `value` when the value is specifically the user's search query.
- Keep search query names consistent across routes, templates, and links.
- Escape rendered values through Jinja defaults; do not mark user search text as safe.
- Pair with `backend-pagination` when search results span multiple pages.
- Pair with `error-handling` for empty results, invalid responses, and API failures.
- Pair with `code-commenting` where search and pagination interact.

## Empty Query Behavior

Use one clear behavior:

- Empty `q` shows the normal product list.
- Non-empty `q` calls the search endpoint.
- No results shows a friendly empty state while keeping the search box populated.

## Before Finishing

- Confirm searches work with spaces and special characters.
- Confirm clearing the search returns to the normal list.
- Confirm page links keep the search query.
- Confirm the search form submits through Flask and triggers a backend API request.
- Confirm search behavior reuses shared helpers where it can.
