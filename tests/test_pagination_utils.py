from app.utils.pagination import build_pagination, calculate_skip, parse_page_number


def test_parse_page_number_defaults_invalid_values_to_first_page():
    # Missing, non-numeric, and negative page values should never crash the route.
    assert parse_page_number(None) == 1
    assert parse_page_number("abc") == 1
    assert parse_page_number("-4") == 1


def test_calculate_skip_converts_page_to_dummyjson_offset():
    # DummyJSON uses skip/limit, so page 3 with 10 items skips the first 20.
    assert calculate_skip(page=1, limit=10) == 0
    assert calculate_skip(page=3, limit=10) == 20


def test_build_pagination_returns_previous_and_next_pages():
    # With 25 products and 10 per page, page 2 has both previous and next links.
    pagination = build_pagination(page=2, total=25, limit=10)

    assert pagination.page == 2
    assert pagination.total_pages == 3
    assert pagination.prev_page == 1
    assert pagination.next_page == 3


def test_build_pagination_clamps_page_to_last_available_page():
    # Very large page numbers are corrected to the last real page.
    pagination = build_pagination(page=99, total=25, limit=10)

    assert pagination.page == 3
    assert pagination.prev_page == 2
    assert pagination.next_page is None
