---
name: code-commenting
description: Add simple, understandable comments to project files for the Flask DummyJSON products assignment. Use when creating, editing, or reviewing code and the user asks for comments, documentation inside files, clearer explanations, beginner-friendly code, comments in every relevant file, or easier-to-read assignment code.
---

# Code Commenting

## Purpose

Make code easier for a new reader to understand without filling files with obvious comments.

## Responsibilities

- Add a short file-level comment to changed source files when the file purpose is not already obvious.
- Add comments before important blocks of logic.
- Explain why the block exists or what responsibility it has.
- Keep comments simple, direct, and beginner-friendly.
- Update old comments when changing nearby code.

## Good Places For Comments

- Flask route decisions and request parameter handling.
- External API calls and response transformations.
- Pagination calculations such as `skip` and total pages.
- Search behavior, especially where it combines with pagination.
- Template sections that depend on specific backend context.
- Gallery event handling and DOM updates.
- Error handling and fallback behavior.
- Assignment-specific decisions, such as keeping API calls/search/pagination in the backend.
- Project setup decisions, such as using `uv` for Python dependencies.
- Non-obvious naming choices when a short name is required by a framework or API.

## Rules

- Prefer one or two short sentences.
- Use the same comment style as the file's language.
- Avoid comments that repeat the exact code.
- Do not add comments to generated files, dependency folders, lockfiles, minified files, or obvious boilerplate.
- Remove comments that become false, redundant, or distracting.

## Good Comment Style

```python
# Convert the external API response into the shape the template expects.
```

```javascript
// Keep the selected image in sync with the thumbnail the user clicked.
```

Avoid:

```python
# Set page to page.
```

```javascript
// Add one to index.
```

## Before Finishing

- Check each edited source file for at least one helpful comment when it contains real logic.
- Read comments together with the code and remove anything that feels noisy.
- Confirm comments explain intent, not syntax.
