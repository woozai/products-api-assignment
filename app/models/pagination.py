from dataclasses import dataclass


@dataclass(frozen=True)
class Pagination:
    """Normalized pagination data used by routes and templates."""

    page: int
    limit: int
    total: int
    total_pages: int
    prev_page: int | None = None
    next_page: int | None = None
