from math import ceil

from app.models import Pagination

PRODUCTS_PER_PAGE = 10


def parse_page_number(raw_page: str | None) -> int:
    """Read a user-provided page number and fall back to the first page."""
    try:
        page = int(raw_page or 1)
    except ValueError:
        return 1

    return max(page, 1)


def calculate_skip(page: int, limit: int = PRODUCTS_PER_PAGE) -> int:
    """Convert a 1-based page number into DummyJSON's skip value."""
    return (page - 1) * limit


def calculate_total_pages(total: int, limit: int = PRODUCTS_PER_PAGE) -> int:
    if total <= 0:
        return 1

    return ceil(total / limit)


def build_pagination(page: int, total: int, limit: int = PRODUCTS_PER_PAGE) -> Pagination:
    total_pages = calculate_total_pages(total, limit)
    current_page = min(page, total_pages)

    return Pagination(
        page=current_page,
        limit=limit,
        total=total,
        total_pages=total_pages,
        prev_page=current_page - 1 if current_page > 1 else None,
        next_page=current_page + 1 if current_page < total_pages else None,
    )
