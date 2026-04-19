from app import create_app
from app.models import ProductPage


def build_empty_product_page(total=0, skip=0, limit=10):
    """Build the service result shape that the route expects."""
    return ProductPage(products=[], total=total, skip=skip, limit=limit)


def test_products_route_uses_list_endpoint_when_query_is_empty(monkeypatch):
    import app.routes.products as products_route

    captured_call = {}

    def fake_list_products(limit, skip):
        # Capture the route's service call without calling DummyJSON.
        captured_call["limit"] = limit
        captured_call["skip"] = skip
        return build_empty_product_page(total=0, skip=skip, limit=limit)

    monkeypatch.setattr(products_route, "list_products", fake_list_products)

    # Flask's test client calls the route without starting a real server.
    response = create_app().test_client().get("/")

    # Empty q should use the normal listing flow and render the empty-state text.
    assert response.status_code == 200
    assert captured_call == {"limit": 10, "skip": 0}
    assert "No products are available right now." in response.get_data(as_text=True)


def test_products_route_uses_search_endpoint_when_query_is_present(monkeypatch):
    import app.routes.products as products_route

    captured_call = {}

    def fake_search_products(query, limit, skip):
        # Capture the search query and pagination values sent by the route.
        captured_call["query"] = query
        captured_call["limit"] = limit
        captured_call["skip"] = skip
        return build_empty_product_page(total=0, skip=0, limit=limit)

    monkeypatch.setattr(products_route, "search_products", fake_search_products)

    response = create_app().test_client().get("/?q= phone &page=2")

    # The route trims search text, calculates skip, and keeps q visible in HTML.
    assert response.status_code == 200
    assert captured_call == {"query": "phone", "limit": 10, "skip": 10}
    assert 'value="phone"' in response.get_data(as_text=True)
    assert "No products found for" in response.get_data(as_text=True)
    assert "phone" in response.get_data(as_text=True)


def test_products_route_redirects_out_of_range_page_to_last_page(monkeypatch):
    import app.routes.products as products_route

    captured_call = {}

    def fake_list_products(limit, skip):
        # 25 total products with a page size of 10 means the last page is 3.
        captured_call["limit"] = limit
        captured_call["skip"] = skip
        return build_empty_product_page(total=25, skip=skip, limit=limit)

    monkeypatch.setattr(products_route, "list_products", fake_list_products)

    response = create_app().test_client().get("/?page=99")

    # The user should be redirected to the last valid page instead of seeing junk.
    assert response.status_code == 302
    assert response.headers["Location"] == "/?page=3"
    assert captured_call == {"limit": 10, "skip": 980}


def test_products_route_hides_raw_service_errors(monkeypatch):
    import app.routes.products as products_route
    from app.services.products import ProductServiceError

    def fake_list_products(limit, skip):
        # This simulates a backend failure with technical details.
        assert limit == 10
        assert skip == 0
        raise ProductServiceError("internal API detail")

    monkeypatch.setattr(products_route, "list_products", fake_list_products)

    response = create_app().test_client().get("/")
    page_html = response.get_data(as_text=True)

    # Users see a friendly message, not the internal error text.
    assert response.status_code == 200
    assert "Products are temporarily unavailable. Please try again later." in page_html
    assert "internal API detail" not in page_html
