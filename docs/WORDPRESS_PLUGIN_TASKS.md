# WordPress Plugin Bonus Plan

## Goal

Build the optional WordPress plugin version of the DummyJSON products assignment while keeping it fully separate from the Flask app.

The plugin should:

- create a WordPress page titled `Compare Assignment` on activation;
- render the assignment product experience through a shortcode on that page;
- fetch DummyJSON products from PHP on the backend;
- support backend search and backend pagination;
- render product rows, thumbnails, and gallery buttons;
- use vanilla JavaScript only for opening and closing rendered gallery images.

## Non-Negotiables

- [ ] Keep all plugin code under `wordpress-plugin/products-assignment/`.
- [ ] Do not mix WordPress code into the Flask `app/` folder.
- [ ] Do not call DummyJSON from browser JavaScript.
- [ ] Do not implement frontend search or frontend pagination.
- [ ] Do not add frontend frameworks.
- [ ] Do not add WordPress tests unless explicitly requested.
- [ ] Keep the plugin readable, modular, and easy to manually verify.

## Target Structure

```text
wordpress-plugin/
`-- products-assignment/
    |-- products-assignment.php
    |-- uninstall.php
    |-- includes/
    |   |-- activation.php
    |   |-- assets.php
    |   |-- dummyjson-api.php
    |   |-- pagination.php
    |   |-- products.php
    |   `-- shortcode.php
    |-- assets/
    |   |-- css/
    |   |   `-- products-assignment.css
    |   `-- js/
    |       `-- gallery.js
    `-- templates/
        `-- products-table.php
```

## Key Decisions

- [ ] Plugin folder: `products-assignment`.
- [ ] Main plugin file: `products-assignment.php`.
- [ ] Generated page title: `Compare Assignment`.
- [ ] Shortcode: `[products_assignment]`.
- [ ] Query parameter for search: `q`.
- [ ] Query parameter for pagination: `product_page`.
- [ ] Page size: use one fixed limit, preferably `10`, unless the Flask app already documents a different assignment limit.
- [ ] Store only the generated page ID in WordPress options.
- [ ] Do not add a settings screen for the first implementation.
- [ ] Do not add persistent caching for the first implementation.

## Phase 1: Bootstrap And Boundaries

Purpose: create the plugin shell with predictable loading and no heavy work at file load time.

- [x] Create `wordpress-plugin/products-assignment/products-assignment.php`.
- [x] Add a valid WordPress plugin header.
- [x] Define constants for plugin version, path, URL, shortcode name, page title, option name, and page size.
- [x] Require focused files from `includes/`.
- [x] Register activation and deactivation hooks at top-level scope.
- [x] Register the shortcode from an `init` hook.
- [x] Keep admin-only activation/page logic out of frontend rendering.

Done when:

- [x] WordPress can detect the plugin.
- [x] Loading the main file does not perform remote requests or create pages.

## Phase 2: Activation, Page Creation, And Uninstall

Purpose: make activation useful and safe without creating duplicate content.

- [x] Create `includes/activation.php`.
- [x] On activation, look up an existing page titled `Compare Assignment`.
- [x] If no matching page exists, create one with `[products_assignment]` as the content.
- [x] Store the created or matched page ID in a plugin option.
- [x] Avoid duplicate pages across repeated activation.
- [x] Leave user-edited page content alone after the first creation.
- [x] Create `uninstall.php`.
- [x] On uninstall, delete only the plugin option.
- [x] Do not delete the generated page automatically unless the user explicitly asks for destructive cleanup.

Done when:

- [x] Activating twice leaves only one `Compare Assignment` page.
- [x] Uninstall removes plugin-owned options and does not remove user content.

## Phase 3: Product Data Layer

Purpose: isolate all DummyJSON behavior behind small PHP helpers.

- [x] Create `includes/dummyjson-api.php`.
- [x] Define the DummyJSON base URL in one place.
- [x] Use `/products` for normal listing.
- [x] Use `/products/search` when `q` is not empty.
- [x] Send `limit`, `skip`, and `q` through `add_query_arg()`.
- [x] Fetch with `wp_remote_get()`.
- [x] Set a short request timeout.
- [x] Validate `WP_Error`, HTTP status, JSON parse result, and response shape.
- [x] Return a predictable result array containing products, total, skip, limit, and optional error text.
- [x] Do not expose raw remote error details to visitors.

Done when:

- [x] The shortcode can request products without knowing endpoint details.
- [x] API failures become friendly UI messages instead of PHP warnings.

## Phase 4: Product Normalization

Purpose: keep templates simple and safe by preparing every product before rendering.

- [x] Create `includes/products.php`.
- [x] Normalize title, description, price, rating, stock, brand, category, thumbnail, and images.
- [x] Provide clear fallbacks for missing fields.
- [x] Cast numbers to predictable display values.
- [x] Keep at most 3 gallery image URLs per product.
- [x] Allow only `http` and `https` image URLs.
- [x] Prefer thumbnail as a fallback gallery image when the image list is empty.

Done when:

- [x] The template never needs to inspect raw DummyJSON arrays directly.
- [x] Missing or malformed product fields still render gracefully.

## Phase 5: Request Parsing And Pagination

Purpose: keep backend search and pagination deterministic.

- [x] Create `includes/pagination.php`.
- [x] Read search text from `$_GET['q']`.
- [x] Use `wp_unslash()` before sanitizing input.
- [x] Sanitize search text with WordPress sanitization functions.
- [x] Trim whitespace.
- [x] Read page number from `$_GET['product_page']`.
- [x] Default missing, non-numeric, or low page values to `1`.
- [x] Calculate `skip = (page - 1) * limit`.
- [x] Calculate total pages from the DummyJSON `total` value.
- [x] Clamp impossible page numbers where practical after total is known.
- [x] Preserve the active search query in previous, next, and page links.

Done when:

- [x] Search and pagination are handled by PHP request/response flow.
- [x] Bad query strings do not crash or generate broken links.

## Phase 6: Shortcode Orchestration

Purpose: connect request parsing, API calls, normalization, assets, and template rendering.

- [x] Create `includes/shortcode.php`.
- [x] Register `[products_assignment]`.
- [x] Parse the current search and page values.
- [x] Fetch products from the data layer.
- [x] Normalize returned products before rendering.
- [x] Build pagination data for the template.
- [x] Enqueue plugin CSS and JavaScript only when the shortcode renders.
- [x] Use output buffering for template rendering.
- [x] Pass prepared variables into `templates/products-table.php`.

Done when:

- [x] Adding `[products_assignment]` to any page renders the product UI.
- [x] Pages without the shortcode do not load plugin assets.

## Phase 7: Template Rendering

Purpose: render assignment-required UI with strict escaping.

- [x] Create `templates/products-table.php`.
- [x] Render a GET search form using `q`.
- [x] Render required columns: Title, Description, Price, Rating, Stock, Brand, Category, Thumbnail, and Gallery.
- [x] Display thumbnails with useful `alt` text.
- [x] Render a `Gallery` button for each product row.
- [x] Put prepared image URLs into safe `data-` attributes.
- [x] Render empty search results clearly.
- [x] Render API failure messages without raw exception details.
- [x] Render pagination links only when useful.
- [x] Escape text with `esc_html()` or `esc_attr()`.
- [x] Escape URLs with `esc_url()`.

Done when:

- [x] The table matches the assignment columns.
- [x] Every dynamic value is escaped at output time.

## Phase 8: Gallery JavaScript

Purpose: implement only the required browser-side interaction.

- [x] Create `assets/js/gallery.js`.
- [x] Use vanilla JavaScript.
- [x] Attach listeners to rendered gallery buttons.
- [x] Read image URLs only from button data attributes.
- [x] Insert a gallery row directly after the clicked product row.
- [x] Show up to 3 rendered product images.
- [x] Close the gallery when the same button is clicked again.
- [x] Keep only one gallery open at a time.
- [x] Handle fewer than 3 images.
- [x] Show a friendly fallback when no images are available.
- [x] Do not fetch DummyJSON or any product data from JavaScript.

Done when:

- [x] Gallery behavior works from already-rendered HTML data.
- [x] Opening and closing galleries does not shift unrelated controls unexpectedly.

## Phase 9: Styling

Purpose: keep the bonus UI simple, readable, and assignment-friendly.

- [x] Create `assets/css/products-assignment.css`.
- [x] Style the search form, table, pagination, messages, thumbnails, and gallery row.
- [x] Keep table content readable on smaller screens.
- [x] Use border radius of `6px` or less.
- [x] Avoid decorative or overbuilt landing-page styling.
- [x] Avoid styles that depend on a specific WordPress theme.

Done when:

- [x] The shortcode output remains usable in a plain default WordPress theme.

## Phase 10: Security Review

Purpose: catch WordPress-specific mistakes before calling the plugin done.

- [x] Sanitize all input from `$_GET`.
- [x] Escape all output in templates.
- [x] Escape all generated links and image URLs.
- [x] Reject unsafe image URL schemes.
- [x] Keep remote API details out of user-facing errors.
- [x] Use capability checks for any future admin action.
- [x] Use nonces only if adding future state-changing frontend/admin actions.
- [x] Avoid direct SQL because this plugin does not need custom database queries.

Done when:

- [x] The plugin follows the WordPress sanitize early, escape late pattern.

## Phase 11: README Update

Purpose: document the bonus without confusing it with the Flask assignment.

- [x] Update `README.md` with a WordPress plugin bonus section.
- [x] Explain the plugin path: `wordpress-plugin/products-assignment/`.
- [x] Explain how to copy or symlink the plugin into `wp-content/plugins/`.
- [x] Explain that activation creates the `Compare Assignment` page.
- [x] Document the shortcode `[products_assignment]`.
- [x] State that DummyJSON requests, search, and pagination happen in PHP.
- [x] State that gallery JavaScript only uses data rendered by PHP.
- [x] Keep the existing Flask setup instructions unchanged.

Done when:

- [x] A reviewer can run the Flask app or inspect the WordPress bonus without mixing the two.

## Phase 12: Manual Verification

Purpose: verify the bonus in a real WordPress install.

- [ ] Copy or symlink `wordpress-plugin/products-assignment/` into `wp-content/plugins/`.
- [ ] Activate the plugin in WordPress admin.
- [ ] Confirm the `Compare Assignment` page is created.
- [ ] Reactivate the plugin and confirm no duplicate page appears.
- [ ] Open the generated page.
- [ ] Confirm the default product table loads.
- [ ] Search for a product and confirm results come from the backend.
- [ ] Clear search and confirm the normal list returns.
- [ ] Move through pagination and confirm URLs preserve the search query when present.
- [ ] Confirm thumbnails render with useful alt text.
- [ ] Confirm Gallery buttons open and close rows correctly.
- [ ] Confirm JavaScript does not make DummyJSON network requests.
- [ ] Temporarily break the API URL and confirm a friendly error appears.
- [ ] Confirm pages without the shortcode do not enqueue plugin assets.

## Suggested Build Order

1. Bootstrap, activation, and shortcode placeholder.
2. Request parsing and pagination helpers.
3. DummyJSON API client and product normalization.
4. Template rendering.
5. Gallery JavaScript.
6. CSS polish.
7. README update.
8. Manual WordPress verification.

## Out Of Scope For First Implementation

- [ ] Redis, transients, or persistent caching.
- [ ] Custom admin settings pages.
- [ ] Custom database tables.
- [ ] WP-CLI commands.
- [ ] Docker images for WordPress.
- [ ] Deleting generated pages on uninstall.
- [ ] Reusing Flask Python code inside the plugin.
