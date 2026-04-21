---
name: flask-routing
description: Use when creating or modifying Flask routes, route handlers, request query parameters, redirects, and template responses for the DummyJSON products assignment. Trigger for the main product table page, backend search, backend pagination, and routes that connect Flask requests to services and Jinja templates.
---

# Flask Routing

## Purpose

Keep route handlers small and easy to follow. Routes should translate HTTP requests into service calls, then render the product table page.

## Responsibilities

- Define clear Flask routes with readable function names.
- Name route functions by the page or behavior they serve, such as `show_products` or `index_products`, instead of vague names like `handle`.
- Read query parameters such as `page` and `q` from `request.args`.
- Validate and normalize simple request input before passing it deeper.
- Call service/helper functions for product data, search, pagination, or API integration.
- Pass clean template context into `render_template`.
- Use redirects when a request should be normalized, such as invalid page values.
- Support the assignment's main page with product table, search bar, pagination, and gallery-ready product image data.
- Extract reusable parsing or context-building helpers if route functions become long.

## Route Pattern

Prefer this shape:

```python
@app.get("/")
def index():
    page = parse_page(request.args.get("page"))
    query = request.args.get("q", "").strip()
    products, pagination = product_service.get_products(page=page, query=query)
    return render_template("index.html", products=products, pagination=pagination, query=query)
```

## Rules

- Keep business logic out of route functions.
- Implement dynamic features through backend code: API calls, search, and pagination should happen before rendering the template.
- Do not call external APIs directly from Jinja templates.
- Do not rely on frontend JavaScript for search, pagination, or fetching products.
- Do not build large HTML strings in Python route handlers.
- Do not duplicate query parsing or template context construction across routes.
- Do not use vague route/helper names when the purpose can be named directly.
- Keep route return values consistent: template responses for pages, JSON only for intentional API endpoints.
- Pair with `error-handling` when routes accept user input or call services that can fail.
- Pair with `code-commenting` when adding or changing route logic.

## Before Finishing

- Confirm each route has a single clear responsibility.
- Confirm query parameters keep working when omitted.
- Confirm invalid input cannot crash the app.
- Confirm template context names match the Jinja template.
- Confirm the rendered page includes the required table, search form, and pagination data.
- Confirm route handlers are short enough to understand quickly.
