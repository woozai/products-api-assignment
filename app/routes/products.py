from flask import Blueprint, render_template, request

from app.services.products import ProductServiceError, list_products, search_products
from app.utils.pagination import PRODUCTS_PER_PAGE, build_pagination, calculate_skip, parse_page_number

products_bp = Blueprint("products", __name__)


@products_bp.get("/")
def show_products():
    page = parse_page_number(request.args.get("page"))
    search_query = request.args.get("q", "").strip()
    skip = calculate_skip(page, PRODUCTS_PER_PAGE)
    error_message = None
    empty_message = None

    try:
        if search_query:
            product_page = search_products(search_query, limit=PRODUCTS_PER_PAGE, skip=skip)
        else:
            product_page = list_products(limit=PRODUCTS_PER_PAGE, skip=skip)
    except ProductServiceError:
        # Keep the page renderable if DummyJSON is temporarily unavailable.
        products = []
        pagination = build_pagination(page=1, total=0, limit=PRODUCTS_PER_PAGE)
        error_message = "Products are temporarily unavailable. Please try again later."
    else:
        products = product_page.products
        pagination = build_pagination(
            page=page,
            total=product_page.total,
            limit=product_page.limit or PRODUCTS_PER_PAGE,
        )
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
    if search_query:
        return f'No products found for "{search_query}".'

    return "No products are available right now."
