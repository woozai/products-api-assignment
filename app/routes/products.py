from flask import Blueprint, current_app, redirect, render_template, request, url_for

from app.services.products import ProductServiceError, list_products, search_products
from app.utils.pagination import PRODUCTS_PER_PAGE, build_pagination, calculate_skip, parse_page_number

products_bp = Blueprint("products", __name__)


@products_bp.get("/")
def show_products():
    # Read the browser query string, for example: /?q=phone&page=2.
    page = parse_page_number(request.args.get("page"))
    search_query = request.args.get("q", "").strip()

    # DummyJSON expects skip/limit instead of page numbers.
    skip = calculate_skip(page, PRODUCTS_PER_PAGE)
    error_message = None
    empty_message = None

    try:
        # Search and pagination stay in Flask so JavaScript does not fetch products.
        if search_query:
            product_page = search_products(search_query, limit=PRODUCTS_PER_PAGE, skip=skip)
        else:
            product_page = list_products(limit=PRODUCTS_PER_PAGE, skip=skip)
    except ProductServiceError as error:
        # Keep the page renderable if DummyJSON is temporarily unavailable.
        current_app.logger.warning("Product service failed: %s", error)
        products = []
        pagination = build_pagination(page=1, total=0, limit=PRODUCTS_PER_PAGE)
        error_message = "Products are temporarily unavailable. Please try again later."
    else:
        # The service already converted raw API dictionaries into Product objects.
        products = product_page.products
        pagination = build_pagination(
            page=page,
            total=product_page.total,
            limit=PRODUCTS_PER_PAGE,
        )
        # Redirect impossible pages to the last real page instead of rendering empty data.
        if product_page.total > 0 and page != pagination.page:
            return redirect(url_for("products.show_products", page=pagination.page, q=search_query or None))

        # Empty search results are not an error, so they get a normal message.
        if not products:
            empty_message = _build_empty_message(search_query)

    return render_template(
        "index.html",
        products=products,
        pagination=pagination,
        query=search_query,
        error_message=error_message,
        empty_message=empty_message,
    )


def _build_empty_message(search_query: str) -> str:
    """Create the empty-state message shown above the products table."""
    if search_query:
        return f'No products found for "{search_query}".'

    return "No products are available right now."
