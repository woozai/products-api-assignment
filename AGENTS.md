# AGENTS.md

## Project

This is a Flask implementation of the DummyJSON products assignment.

## Core Rules

- Use Flask, Jinja, vanilla JavaScript, and `uv`.
- Keep API calls, search, and pagination in the backend.
- Do not use frontend frameworks.
- Keep files short and focused.
- Avoid duplicated code.
- Prefer modular, reusable helpers over repeating logic.
- Keep code readable and easy to test.
- Use clear names that describe each function, variable, helper, route, model, template block, CSS class, and JavaScript selector by purpose.
- Do not add tests unless the user explicitly asks for tests.
- Put product API logic in a service layer.
- Put gallery behavior in static JavaScript.
- Add simple, useful comments around important logic.
- Update README when setup or behavior changes.

## Design Preference

Choose small, clear modules with one responsibility. If a file starts doing too many jobs, split the behavior into a helper, service, template partial, or static asset.

## Naming Rule

Name things by what they are responsible for. Prefer names like `search_products`, `normalize_product`, `parse_page_number`, and `gallery_button` over vague names like `handle`, `data`, `item`, `do_stuff`, or `btn`.

## Testing Rule

Write code in a testable way, but do not create or add test files unless the user explicitly asks for tests.
