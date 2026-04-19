from dataclasses import dataclass, field


@dataclass(frozen=True)
class Product:
    """Normalized product data from DummyJSON."""

    id: int
    title: str
    description: str
    price: float
    rating: float
    stock: int
    brand: str
    category: str
    thumbnail: str
    images: list[str] = field(default_factory=list)
