# UI Refactor Tasks

## Goal

Improve the product table page so it is easier to scan, clearer on mobile, and more helpful during search, pagination, empty states, errors, and gallery interactions.

Keep this as a UI polish pass only. Do not change backend routes, service logic, search behavior, pagination behavior, cache behavior, or DummyJSON data flow.

## Page Hierarchy

- [x] Change the main heading from `Products Assignment` to a clearer user-facing title such as `Product Browser`.
- [x] Add a short helper sentence under the title.
- [x] Keep the page simple and assignment-friendly.
- [x] Move or restyle the product count/status text so it is easier to notice.
- [x] Keep the existing `pagination.page`, `pagination.total_pages`, and `pagination.total` values.

## Search UX

- [x] Keep the search form as a backend `GET` form.
- [x] Keep the search parameter named `q`.
- [x] Update the placeholder to `Search products by name`.
- [x] Keep the active search query visible after submit.
- [x] Add a visible `Clear search` link only when a search query is active.
- [x] Make sure `Clear search` links back to the normal product listing.
- [x] Preserve the active search query in pagination links.

## Table Readability

- [x] Keep all required columns: Title, Description, Price, Rating, Stock, Brand, Category, Thumbnail.
- [x] Keep the Gallery column.
- [x] Make title and thumbnail easier to scan.
- [x] Improve description readability with better line height and width.
- [x] Keep price formatted as currency.
- [x] Keep rating formatted consistently.
- [x] Keep stock readable.
- [x] Keep the desktop table horizontally readable.
- [x] Keep the mobile card-like layout working.

## Gallery Interaction

- [x] Change button text from `Gallery` to `View gallery`.
- [x] Change the open button text to `Hide gallery`.
- [x] Add an active visual state for the open gallery button.
- [x] Keep one gallery open at a time.
- [x] Keep same-button click toggling the gallery closed.
- [x] Add a small gallery heading such as `Images for Product Name`.
- [x] Keep missing-image fallback text.
- [x] Confirm JavaScript still does not fetch DummyJSON data.
- [x] Keep gallery images limited to up to 3 rendered URLs.

## Messages And States

- [x] Keep friendly error messages.
- [x] Keep friendly empty search/list messages.
- [x] Make normal, empty, and error messages visually distinct.
- [x] Do not expose raw backend errors in the UI.
- [x] Do not change `/favicon.ico` behavior as part of this pass.

## CSS Polish

- [x] Improve spacing between page sections.
- [x] Improve button hover and focus states.
- [x] Improve input focus state.
- [x] Improve pagination link hover and focus states.
- [x] Keep border radius at `6px` or less.
- [x] Avoid a one-color theme.
- [x] Do not add decorative blobs, gradients, or large hero sections.
- [x] Do not add frontend frameworks.
- [x] Keep text readable on mobile without overflow.

## Verification

- [x] Run `uv run pytest`.
- [x] Run `uv run mypy app`.
- [x] Start the app with `uv run flask --app run run`.
- [x] Open `/` and confirm products render.
- [x] Search for `phone` and confirm the query remains visible.
- [x] Click `Clear search` and confirm normal listing returns.
- [x] Use pagination with no search.
- [x] Use pagination with active search.
- [x] Open and close a gallery.
- [x] Open another gallery and confirm the previous one closes.
- [x] Confirm products with no gallery images show fallback text.
- [x] Check mobile width and confirm text does not overflow.
