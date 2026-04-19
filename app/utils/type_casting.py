from typing import Any
from urllib.parse import urlparse


def to_float(value: Any, default: float = 0.0) -> float:
    """Convert API values to floats without letting bad data crash rendering."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def to_int(value: Any, default: int = 0) -> int:
    """Convert API values to integers without raising on missing fields."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def to_str(value: Any, default: str = "N/A") -> str:
    """Convert API values to display-safe strings."""
    if value is None:
        return default

    text = str(value).strip()
    return text or default


def to_str_list(value: Any) -> list[str]:
    """Keep only usable image URLs from an API list value."""
    if not isinstance(value, list):
        return []

    return [item.strip() for item in value if isinstance(item, str) and item.strip()]


def to_safe_image_url(value: Any) -> str:
    """Allow only http/https image URLs to be rendered in img src attributes."""
    image_url = to_str(value, "")
    parsed_url = urlparse(image_url)

    if parsed_url.scheme in {"http", "https"} and parsed_url.netloc:
        return image_url

    return ""


def to_safe_image_urls(value: Any) -> list[str]:
    """Filter gallery image URLs so unsafe URL schemes are ignored."""
    return [image_url for image_url in (to_safe_image_url(item) for item in to_str_list(value)) if image_url]
