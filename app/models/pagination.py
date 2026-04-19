from dataclasses import dataclass


@dataclass(frozen=True)
class Pagination:
    """Normalized pagination data used by routes and templates."""

    page: int
    limit: int
    total: int
    total_pages: int
    has_prev: bool
    has_next: bool
