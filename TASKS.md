# Project Tasks

## Phase 1: Project Setup

- [x] Initialize Python project with `uv`.
- [x] Choose and document the Python version.
- [x] Add Flask dependency with `uv add flask`.
- [x] Add backend HTTP dependency, such as `uv add requests`.
- [x] Add test dependency only if tests are explicitly requested.
- [x] Add lint/format tools if desired, such as `ruff`.
- [x] Create the base project structure.
- [x] Confirm `uv run flask --app app run` can start the app.

## Phase 2: Flask Application Skeleton

- [x] Create `run.py`.
- [x] Configure the Flask app.
- [x] Add a route module for the products page.
- [x] Register the products route blueprint from `app/__init__.py`.
- [x] Move application code into the `app/` package.
- [x] Create `app/models/` for reusable product and pagination data shapes.
- [x] Create `app/templates/base.html`.
- [x] Create `app/templates/index.html`.
- [x] Create `app/static/css/styles.css`.
- [x] Create `app/static/js/gallery.js`.
- [x] Create `app/utils/` for reusable helpers when later phases need them.
- [x] Confirm Flask serves templates and static files correctly.

## Phase 3: DummyJSON Service Layer

- [x] Create `services/products.py`.
- [x] Define the DummyJSON base URL in one place.
- [x] Implement product listing API call using `/products`.
- [x] Implement product search API call using `/products/search`.
- [x] Send `limit`, `skip`, and `q` as request parameters.
- [x] Add request timeouts.
- [x] Validate response status and JSON shape.
- [x] Normalize product fields for template rendering.
- [x] Add fallbacks for missing fields such as brand, category, thumbnail, or images.

## Phase 4: Backend Pagination

- [x] Decide the fixed page size.
- [x] Parse `page` from query parameters.
- [x] Default invalid or missing page values to page `1`.
- [x] Calculate `skip = (page - 1) * limit`.
- [x] Read `total` from DummyJSON.
- [x] Calculate total pages.
- [x] Build pagination metadata for templates.
- [x] Preserve active search query in pagination links.

## Phase 5: Backend Search

- [x] Add a search form using query parameter `q`.
- [x] Trim whitespace from search input.
- [x] Use normal product listing when `q` is empty.
- [x] Use DummyJSON search endpoint when `q` is non-empty.
- [x] Keep search query visible in the search box after submit.
- [x] Ensure search results paginate correctly.
- [x] Add empty search result messaging.

## Phase 6: Product Table Rendering

- [x] Render the required table columns.
- [x] Display thumbnail as an image.
- [x] Add useful `alt` text to thumbnails.
- [x] Add a `Gallery` button to each product row.
- [x] Include image data for the gallery without frontend API calls.
- [x] Render friendly empty and error states.
- [x] Keep the table readable on smaller screens.

## Phase 7: Gallery Interaction

- [x] Attach gallery click listeners in `static/js/gallery.js`.
- [x] Read up to 3 product image URLs from rendered markup.
- [x] Insert a gallery row between the clicked product and the next product.
- [x] Toggle the gallery closed when the same button is clicked again.
- [x] Decide whether opening one gallery closes other open galleries.
- [x] Handle fewer than 3 images.
- [x] Handle missing images with a friendly fallback.
- [x] Confirm JavaScript does not fetch DummyJSON data.

## Phase 8: Error Handling

- [x] Handle invalid page values.
- [x] Handle empty product lists.
- [x] Handle DummyJSON request timeout.
- [x] Handle non-2xx DummyJSON responses.
- [x] Handle invalid JSON.
- [x] Handle missing product fields.
- [x] Show friendly user messages.
- [x] Avoid exposing raw exceptions in the browser.

## Phase 9: Code Comments And Cleanup

- [x] Add simple comments to important logic blocks.
- [x] Add file-level comments where file purpose is not obvious.
- [x] Remove comments that only repeat the code.
- [x] Keep route functions small.
- [x] Keep API logic in the service layer.
- [x] Keep gallery logic in static JavaScript.
- [x] Remove unused imports, dead code, and temporary debug output.

## Phase 10: Testability

- [x] Keep route logic small enough to test later.
- [x] Keep pagination calculations in helper functions.
- [x] Keep product normalization in helper functions.
- [x] Keep DummyJSON calls isolated in the service layer.
- [x] Do not add test files unless explicitly requested.

## Phase 11: README Documentation

- [x] Add project description.
- [x] Add prerequisites, including `uv`.
- [x] Add installation steps using `uv sync`.
- [x] Add local run command.
- [x] Explain how backend API calls, search, and pagination work.
- [x] Explain the gallery JavaScript behavior.
- [x] Document assumptions and important decisions.
- [x] Document known limitations or unimplemented bonus work.

## Phase 12: Local Verification

- [x] Start the app locally.
- [x] Verify default product list loads.
- [x] Verify search works.
- [x] Verify pagination works without search.
- [x] Verify pagination works with search.
- [x] Verify thumbnails render.
- [x] Verify Gallery opens between the clicked row and next row.
- [x] Verify empty/error states are user-friendly.
- [x] Run tests only if tests were explicitly requested and added.
- [ ] Run lint/format checks if configured.

## Phase 13: GitHub Repository Readiness

- [ ] Review `.gitignore`.
- [ ] Decide whether `.codex/skills` should be committed or kept local.
- [ ] Ensure no secrets or local-only files are committed.
- [ ] Commit source code, docs, lockfile, and tests only if tests were explicitly requested.
- [ ] Push to GitHub.
- [ ] Confirm README renders correctly on GitHub.

## Phase 14: CI

- [x] Create `.github/workflows/ci.yml`.
- [x] Configure workflow triggers for push and pull request.
- [x] Install Python.
- [x] Install `uv`.
- [x] Run `uv sync --locked`.
- [x] Run lint/format checks if configured.
- [x] Run `uv run pytest` only if tests were explicitly requested and added.
- [x] Add a simple smoke check if useful.
- [x] Confirm CI passes on GitHub.

## Phase 15: Container Image

- [x] Create a `Dockerfile` for the Flask application.
- [x] Use a slim Python base image that supports Python 3.13.
- [x] Install `uv` inside the image.
- [x] Copy `pyproject.toml` and `uv.lock` before app code to improve Docker layer caching.
- [x] Install locked production dependencies with `uv sync --locked --no-dev`.
- [x] Copy the Flask application code into the image.
- [x] Expose the application port.
- [x] Set the container command to run the Flask app.
- [x] Create a `.dockerignore` file.
- [x] Exclude `.venv`, caches, tests cache, Git files, local AI files, and other local-only files from the image context.
- [x] Build the image locally with a clear name, such as `products-api-assignment`.
- [x] Run the image locally.
- [x] Confirm the containerized app loads in the browser.
- [x] Document Docker build and run commands in README.

## Phase 16: Trivy Security Scanning In CI

- [x] Add a Docker image build step to GitHub Actions.
- [x] Tag the CI image with a local CI tag, such as `products-api-assignment:ci`.
- [x] Add Trivy to the CI workflow.
- [x] Scan the built image with Trivy.
- [x] Fail CI on high and critical vulnerabilities.
- [x] Configure Trivy to scan operating system and library vulnerabilities.
- [x] Keep the scan non-publishing; do not push the image unless deployment is added later.
- [x] Add a Trivy result summary or table output to the GitHub Actions logs.
- [x] Confirm CI still runs `uv sync --locked`, tests, mypy, and Flask route smoke check.
- [ ] Confirm CI fails if Trivy finds high or critical vulnerabilities.
- [x] Document the Trivy scan behavior in README.

## Phase 17: CD

- [ ] Choose deployment target if deployment is required.
- [ ] Add deployment secrets to GitHub Actions.
- [ ] Add a deployment job that runs only after CI passes.
- [ ] Keep deployment config documented in README.
- [ ] Verify deployed app manually.

## Optional Phase: WordPress Plugin Bonus

### WordPress Plugin Structure

- [ ] Create `wordpress-plugin/products-assignment/`.
- [ ] Create `wordpress-plugin/products-assignment/products-assignment.php`.
- [ ] Create `wordpress-plugin/products-assignment/includes/`.
- [ ] Create `wordpress-plugin/products-assignment/assets/css/`.
- [ ] Create `wordpress-plugin/products-assignment/assets/js/`.
- [ ] Create `wordpress-plugin/products-assignment/templates/`.
- [ ] Keep WordPress plugin code separate from the Flask `app/` folder.

### Plugin Bootstrap

- [ ] Add a valid WordPress plugin header in `products-assignment.php`.
- [ ] Define plugin constants for plugin path, plugin URL, version, and shortcode name.
- [ ] Load plugin includes from the main plugin file.
- [ ] Register activation hook.
- [ ] Register shortcode hook.
- [ ] Register frontend CSS and JavaScript assets.

### Auto-Page Creation

- [ ] On plugin activation, check if a page titled `Compare Assignment` already exists.
- [ ] If the page does not exist, create it automatically.
- [ ] Set the page content to render the plugin shortcode.
- [ ] Store the generated page ID in a WordPress option.
- [ ] Avoid creating duplicate pages on repeated activation.
- [ ] Confirm the generated page is publicly viewable.

### Shortcode Integration

- [ ] Create a shortcode, for example `[products_assignment]`.
- [ ] Make the shortcode render the product search form, table, pagination, and gallery buttons.
- [ ] Ensure the auto-created page uses this shortcode.
- [ ] Keep rendering logic in a template file instead of building large HTML strings in PHP.

### DummyJSON API Integration In PHP

- [ ] Create a PHP API helper for DummyJSON requests.
- [ ] Define the DummyJSON base URL in one place.
- [ ] Use `/products` for normal product listing.
- [ ] Use `/products/search` when the search query is not empty.
- [ ] Send `limit`, `skip`, and `q` as request parameters.
- [ ] Use WordPress HTTP functions such as `wp_remote_get`.
- [ ] Add a request timeout.
- [ ] Validate HTTP response status.
- [ ] Validate JSON response shape.
- [ ] Normalize product fields before rendering.
- [ ] Add fallbacks for missing fields such as title, description, brand, category, thumbnail, and images.
- [ ] Allow only safe `http` and `https` image URLs.

### Backend Search And Pagination

- [ ] Read search query from `$_GET['q']`.
- [ ] Sanitize the search query with WordPress sanitization functions.
- [ ] Trim whitespace from the search query.
- [ ] Read page number from `$_GET['product_page']`.
- [ ] Default invalid or missing page values to `1`.
- [ ] Use a fixed page size.
- [ ] Calculate `skip = (page - 1) * limit`.
- [ ] Preserve the active search query in pagination links.
- [ ] Redirect or clamp out-of-range pages safely.

### Product Table Rendering

- [ ] Render the required columns: Title, Description, Price, Rating, Stock, Brand, Category, Thumbnail.
- [ ] Display thumbnail as an image.
- [ ] Add useful `alt` text to thumbnails.
- [ ] Escape all rendered text with WordPress escaping functions.
- [ ] Escape URLs with `esc_url`.
- [ ] Add a `Gallery` button to each row.
- [ ] Include up to 3 product image URLs in rendered data attributes.
- [ ] Render friendly empty and error states.
- [ ] Keep the table readable on smaller screens.

### Gallery JavaScript

- [ ] Add vanilla JavaScript for the Gallery button.
- [ ] Read image URLs from rendered markup.
- [ ] Insert a gallery row between the clicked product and the next product row.
- [ ] Toggle the gallery closed when the same button is clicked again.
- [ ] Opening one gallery closes any other open gallery.
- [ ] Handle fewer than 3 images.
- [ ] Handle missing images with a friendly fallback.
- [ ] Confirm JavaScript does not fetch DummyJSON data.

### WordPress Security

- [ ] Sanitize all input from `$_GET`.
- [ ] Escape all output with `esc_html`, `esc_attr`, and `esc_url`.
- [ ] Use nonces only if adding actions that modify data from the frontend.
- [ ] Avoid exposing raw API errors to users.
- [ ] Avoid rendering unsafe image URL schemes.
- [ ] Do not store API secrets because DummyJSON does not require them.
- [ ] Do not use frontend frameworks.

### WordPress Documentation

- [ ] Update README with a bonus WordPress section.
- [ ] Explain where the plugin folder lives.
- [ ] Explain how to install the plugin into `wp-content/plugins/`.
- [ ] Explain that activation creates the `Compare Assignment` page.
- [ ] Explain the shortcode used by the page.
- [ ] Document assumptions and limitations of the WordPress bonus.

### WordPress Manual Verification

- [ ] Copy or symlink `wordpress-plugin/products-assignment/` into a local WordPress `wp-content/plugins/` folder.
- [ ] Activate the plugin from the WordPress admin.
- [ ] Confirm the `Compare Assignment` page is created once.
- [ ] Open the generated page.
- [ ] Confirm the product table loads.
- [ ] Confirm backend search works.
- [ ] Confirm pagination works.
- [ ] Confirm thumbnails render.
- [ ] Confirm Gallery buttons work.
- [ ] Confirm empty search results show a friendly message.
- [ ] Confirm API failure does not expose raw errors.
