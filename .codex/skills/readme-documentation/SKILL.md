---
name: readme-documentation
description: Use when creating or updating README documentation for the Flask DummyJSON products assignment, including uv-based installation instructions, local run steps, app explanation, assumptions, important decisions, requirements coverage, and submission readiness.
---

# README Documentation

## Purpose

Make the project easy for an evaluator to install, run, and understand.

## Required Sections

- Project title and short description.
- Installation instructions.
- Local run instructions.
- Brief explanation of how the application works.
- Assumptions and important decisions.
- Requirements coverage or feature checklist.

## Content Rules

- Keep instructions copy-paste friendly.
- Mention Python version expectations if known.
- Use `uv` for Python package installation, environment management, and run commands.
- Prefer commands such as `uv sync`, `uv add <package>`, and `uv run flask --app app run`.
- Do not default to `pip install -r requirements.txt` unless the project intentionally includes a requirements export.
- Mention virtual environment setup only when it is needed beyond `uv sync`.
- Explain that DummyJSON API calls, search, and pagination are handled by the backend.
- Mention that the Gallery button uses vanilla JavaScript.
- Mention the code organization approach: small files, modular services/helpers, no duplicated logic, readable and testable code.
- Mention tests only if the user explicitly requested tests or test files exist.
- Document any known limitations or bonus work not completed.

## Before Finishing

- Confirm commands match the actual file structure.
- Confirm README commands use `uv`.
- Confirm README does not promise features that are not implemented.
- Confirm assumptions are honest and specific.
