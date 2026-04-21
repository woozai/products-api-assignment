---
name: backend-pagination
description: Use when implementing or changing backend pagination for the DummyJSON products table, search results, Flask query parameters, API `limit`/`skip` values, page counts, previous/next links, or Jinja pagination controls. Do not use for client-side pagination; the assignment requires backend pagination.
---

# Backend Pagination

## Purpose

Make pagination predictable, server-driven, and compatible with the external products API.

## Responsibilities

- Read `page` from the request and default to page `1`.
- Convert page numbers into API `skip` and `limit` values.
- Calculate pagination metadata for templates.
- Preserve search query parameters while moving between pages.
- Prevent invalid page values from crashing the app.
- Keep pagination working for both the normal product list and search results.
- Keep pagination parsing and calculations in small reusable helpers when used in more than one place.
- Name pagination helpers by their exact purpose, such as `parse_page_number`, `calculate_skip`, or `build_pagination`.

## Calculation Rules

- Use a fixed `limit` unless the assignment or user asks otherwise.
- Treat pages as 1-based in URLs and templates.
- Calculate `skip` as `(page - 1) * limit`.
- Calculate total pages with ceiling division when `total` is available.
- Clamp or redirect invalid pages based on the existing app pattern.

## Template Context

Pass simple pagination data to templates, for example:

```python
pagination = {
    "page": page,
    "limit": limit,
    "total": total,
    "total_pages": total_pages,
    "has_prev": page > 1,
    "has_next": page < total_pages,
}
```

## Rules

- Do not fetch every product and slice locally when the API supports pagination.
- Do not lose the active search query when generating next or previous links.
- Do not implement page switching only in JavaScript.
- Do not duplicate pagination calculations across route handlers, services, and templates.
- Do not hide pagination meaning behind generic names like `calc`, `numbers`, or `meta`.
- Keep page parsing in one helper when multiple routes need it.
- Pair with `backend-api-integration` when passing `limit` and `skip` to the API.
- Pair with `jinja-rendering` when updating pagination controls.
- Pair with `code-commenting` around calculations that may be confusing to beginners.

## Before Finishing

- Manually verify first page, middle page, last page, and invalid page input unless tests are explicitly requested.
- Confirm pagination links preserve `q` or other active filters.
- Confirm empty result sets do not produce broken links.
- Confirm pagination requests call DummyJSON with the correct `skip` and `limit`.
- Confirm pagination helpers can be tested without calling Flask or DummyJSON.
