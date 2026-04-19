from dataclasses import dataclass

from app.models.product import Product


@dataclass(frozen=True)
class ProductPage:
    """Normalized page of products returned by DummyJSON."""

    products: list[Product]
    total: int
    skip: int
    limit: int
