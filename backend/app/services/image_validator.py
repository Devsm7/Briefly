"""Validate image URLs — returns placeholder if the URL is missing, broken, or not an image."""

import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

from app.services.image_constants import PLACEHOLDER_IMAGE_URL

logger = logging.getLogger(__name__)

_TIMEOUT = 5
_IMAGE_CONTENT_TYPES = ("image/jpeg", "image/png", "image/webp", "image/gif", "image/avif")


def is_valid_image_url(url: str | None) -> bool:
    """
    Return True only if url resolves to a real image.
    Uses a HEAD request first; falls back to GET if the server doesn't support HEAD.
    """
    if not url or url == PLACEHOLDER_IMAGE_URL:
        return False
    try:
        resp = requests.head(url, timeout=_TIMEOUT, allow_redirects=True)
        if resp.status_code == 405:
            resp = requests.get(url, timeout=_TIMEOUT, allow_redirects=True, stream=True)
        if not resp.ok:
            return False
        content_type = resp.headers.get("Content-Type", "")
        return any(content_type.startswith(ct) for ct in _IMAGE_CONTENT_TYPES)
    except Exception:
        return False


def resolve_image_url(url: str | None) -> str:
    """Return the url if valid, otherwise return the placeholder."""
    return url if is_valid_image_url(url) else PLACEHOLDER_IMAGE_URL
