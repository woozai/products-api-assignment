---
name: assignment-requirements
description: Use when planning, implementing, reviewing, or verifying the Flask DummyJSON products assignment against the provided requirements, including uv Python packaging, backend data retrieval, dynamic table generation, backend search, backend pagination, gallery button behavior, README documentation, and optional WordPress plugin bonus.
---

# Assignment Requirements

## Purpose

Use this as the source-of-truth checklist for the selected Flask implementation.

## Required Features

- Build a Flask web application.
- Use `uv` for Python dependency management and local run commands.
- Fetch product data from DummyJSON in the backend.
- Dynamically render a page with a products table.
- Include a search bar that uses the DummyJSON search API through the backend.
- Include backend pagination.
- Add a Gallery button in each product row.
- Use vanilla JavaScript for the gallery interaction.
- Provide a README with setup, explanation, assumptions, and decisions.

## Required Table Columns

- Title
- Description
- Price
- Rating
- Stock
- Brand
- Category
- Thumbnail as an image

## Backend Rules

- Implement API calls, pagination, and search in Python/Flask.
- Do not use frontend JavaScript to fetch, search, or paginate products.
- Keep DummyJSON integration in a service/helper layer.
- Keep files small, modular, reusable, testable, and readable.
- Use clear, purpose-revealing names for functions, variables, helpers, routes, models, HTML elements, CSS classes, and JavaScript selectors.
- Avoid duplicated code, especially around API calls, pagination calculations, query parsing, and product normalization.
- Do not add tests unless the user explicitly asks for tests.
- Handle incorrect or missing inputs gracefully.

## Frontend Rules

- Do not use frontend frameworks.
- Use Jinja for dynamic HTML rendering.
- Use JavaScript only for the Gallery button interaction.
- Insert the gallery tab/row between the clicked product and the next product.
- Show up to 3 product images when they exist.

## Completion Checklist

- Normal product list loads.
- Search returns matching products.
- Pagination works for list and search results.
- Required table columns are visible.
- Thumbnail images render.
- Gallery button opens the correct images in the correct location.
- Empty results and API failures do not crash the app.
- README explains how to install and run locally.
- README and project files use `uv` commands instead of defaulting to `pip`.
- Code is organized into focused files without unnecessary duplication.
