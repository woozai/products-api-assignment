---
name: error-handling
description: Use when handling DummyJSON API failures, invalid Flask query parameters, missing product fields, empty search results, bad pagination values, HTTP errors, JSON parsing problems, broken image data, fallback UI, or any code path that should fail gracefully instead of crashing the products assignment app.
---

# Error Handling

## Purpose

Make the app resilient and user-friendly when inputs are invalid or the external API does not behave as expected.

## Responsibilities

- Validate user-controlled values such as `page` and `q`.
- Handle network timeouts, non-2xx responses, invalid JSON, and missing API fields.
- Return safe default data shapes to routes and templates.
- Show useful messages instead of raw tracebacks.
- Log or preserve technical detail where it helps debugging, without exposing it to users.
- Keep the product table page renderable even when the API returns no products or partial product data.

## Backend Rules

- Use request timeouts for external API calls.
- Catch specific exceptions when practical.
- Keep fallback return values compatible with normal template rendering.
- Do not silently swallow errors that make debugging impossible.
- Do not show raw exception text in the browser.
- Pair with `backend-api-integration` for external API calls.
- Pair with `flask-routing` for invalid query parameters.
- Pair with `jinja-rendering` for empty and error states.

## Common Cases

- Invalid page: default to page `1`, clamp, or redirect according to the app pattern.
- Empty search results: show a friendly message and keep the search query visible.
- API unavailable: show a fallback page state and avoid crashing.
- Missing product image: render a placeholder or skip the broken image.
- Missing product field: render a sensible fallback such as `N/A`.

## Before Finishing

- Confirm templates can render fallback data.
- Confirm users see clear, non-technical messages.
- Confirm the developer still has enough information to debug failures.
- Confirm API errors do not break search or pagination controls.
