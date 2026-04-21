---
name: project-structure
description: Use when creating, organizing, or refactoring the Flask DummyJSON products assignment file structure, including app entry points, services, templates, static JavaScript/CSS, uv Python packaging, configuration, requirements, README, and separation of backend routes, API integration, Jinja templates, and frontend gallery behavior.
---

# Project Structure

## Purpose

Keep the assignment project easy to navigate by putting each responsibility in the right place.

## Suggested Layout

Use the existing project layout if one already exists. For a new simple Flask app, prefer a structure like:

```text
.
|-- app.py
|-- pyproject.toml
|-- uv.lock
|-- README.md
|-- services/
|   `-- products.py
|-- templates/
|   `-- index.html
`-- static/
    |-- css/
    |   `-- styles.css
    `-- js/
        `-- gallery.js
```

## Responsibilities

- Put Flask route handlers in the app entry point or routes module.
- Put external API calls and product data shaping in a backend service module.
- Put HTML rendering in Jinja templates.
- Put gallery click behavior in static JavaScript.
- Put styling in static CSS.
- Use `uv` for Python dependency management and local commands.
- Prefer `pyproject.toml` and `uv.lock` over a manually maintained `requirements.txt`.
- Keep README setup instructions at the project root.
- Keep files short, focused, and easy to scan.
- Split repeated behavior into reusable helpers, services, template partials, or JavaScript functions.
- Prefer modular code that can be tested without starting the whole app.
- Do not create test files unless the user explicitly asks for tests.
- Use names that describe purpose clearly for modules, functions, helpers, models, templates, CSS classes, and JavaScript selectors.

## Rules

- Keep files small enough to read comfortably.
- Do not mix API fetching, HTML templates, and frontend event handling in one place.
- Do not duplicate route, API, pagination, search, or DOM-manipulation logic across files.
- Do not create large files that handle unrelated responsibilities.
- Prefer clear names over clever abstractions.
- Avoid vague names such as `data`, `item`, `helper`, `thing`, `handle`, or `btn` when a more specific name is available.
- Do not add a frontend framework for this assignment.
- Do not introduce a different Python package manager unless the user asks.
- Follow existing structure first if the project already has one.
- Pair with the specific domain skill for the part being changed, such as `flask-routing`, `backend-api-integration`, or `gallery-interaction`.
- Pair with `code-commenting` when creating or reorganizing source files.

## Before Finishing

- Confirm imports still work from the project root.
- Confirm Flask can find `templates/` and `static/`.
- Confirm every file has one clear job.
- Confirm the project can be run locally from the README instructions.
- Confirm Python dependencies and run commands use `uv`.
- Confirm repeated logic has been extracted instead of copied.
- Confirm important behavior can be unit tested in small pieces.
- Confirm no test files were added unless explicitly requested.
