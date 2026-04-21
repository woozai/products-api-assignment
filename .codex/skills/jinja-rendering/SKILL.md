---
name: jinja-rendering
description: Use when creating or modifying Flask Jinja templates for the DummyJSON products assignment, including the required product table columns, search form, pagination controls, empty/error states, gallery markup, template inheritance, and safe display of backend data. Do not use for service-layer business logic.
---

# Jinja Rendering

## Purpose

Keep templates readable and focused on displaying data already prepared by Flask routes and services.

## Responsibilities

- Render product data with simple loops and conditionals.
- Display search input values, product lists, pagination, errors, and empty states.
- Use template inheritance or partials if the project already uses them.
- Keep form and link query parameters consistent with Flask routes.
- Render gallery data in a way frontend JavaScript can use without extra API calls.
- Render the required table columns: Title, Description, Price, Rating, Stock, Brand, Category, and Thumbnail.
- Add a Gallery button for each product row.

## Rules

- Keep complex calculations in Python, not Jinja.
- Do not call external APIs from templates.
- Do not put large JavaScript logic directly inside templates if a static JS file exists.
- Do not implement assignment-required search or pagination purely in frontend JavaScript.
- Use Jinja's default escaping for user-controlled values.
- Use clear names like `products`, `pagination`, `query`, and `error`.
- Use purpose-revealing element names and CSS classes, such as `products-table`, `search-form`, `pagination-link`, and `gallery-button`.
- Pair with `backend-pagination` for pagination controls.
- Pair with `gallery-interaction` for markup used by product image toggles.
- Pair with `code-commenting` for non-obvious template sections.

## Product Display Guidance

- Show only fields the backend guarantees are present or safely defaulted.
- Use fallback text when optional fields such as brand, category, rating, or images are missing.
- Keep repeated row/card markup consistent.
- Render thumbnail values as image elements with useful alt text.

## Before Finishing

- Confirm every template variable is supplied by its route.
- Confirm empty lists and API errors render a useful message.
- Confirm generated links keep active search and pagination state.
- Confirm every row includes the required product data and a Gallery button.
