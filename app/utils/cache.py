def build_products_cache_key(api_mode: str, *, query: str = "", limit: int, skip: int) -> str:
    """Build a stable cache key for product listing and search requests."""
    normalized_query = query.strip().lower()
    return f"products:{api_mode}:q={normalized_query}:limit={limit}:skip={skip}"
