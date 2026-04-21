---
name: gallery-interaction
description: Use when implementing or changing the assignment's vanilla JavaScript Gallery button behavior, including inserting a tab/row between the clicked product and the next product, showing up to 3 product images, toggling galleries, and using Jinja-rendered image data. Do not use frontend frameworks or browser-side product API fetching.
---

# Gallery Interaction

## Purpose

Provide a simple frontend interaction for showing product images that were already delivered by the backend template.

## Responsibilities

- Add click handlers for product gallery buttons.
- Show, hide, or toggle a gallery tab/row directly between the clicked table row and the next product row.
- Display a small number of product images, commonly up to 3.
- Keep DOM selectors stable and easy to understand.
- Name JavaScript functions and selectors by purpose, such as `toggleProductGallery`, `createGalleryRow`, and `.gallery-button`.
- Preserve accessibility basics for buttons and images.
- Split DOM selection, gallery row creation, and toggle behavior into small readable functions if the script grows.

## Rules

- Use vanilla JavaScript unless the project already uses a framework.
- Do not use frontend frameworks.
- Do not fetch product data from JavaScript when the backend already supplies it.
- Store image URLs in rendered markup, data attributes, or nearby hidden template data.
- Keep state simple: the clicked product opens or closes its gallery.
- Avoid global state unless it makes the interaction simpler and clearer.
- Avoid duplicating DOM creation logic for each image.
- Avoid vague names like `btn`, `el`, `x`, or `doGallery` when a clearer name fits.
- Pair with `jinja-rendering` when the template must expose image data.
- Pair with `code-commenting` for event flow or DOM construction that is not obvious.

## UI Behavior

- A second click on the same gallery button should close it, unless the assignment says otherwise.
- If opening one gallery should close another, implement that behavior explicitly and simply.
- Missing images should show a friendly fallback instead of a broken layout.
- The gallery should show 3 images when 3 exist, fewer when fewer exist.

## Before Finishing

- Confirm gallery buttons work after page load.
- Confirm products with fewer than 3 images still render correctly.
- Confirm generated image tags include useful `alt` text.
- Confirm the gallery appears between the clicked row and the next product row.
- Confirm the JavaScript remains small, readable, and testable by inspection.
