"""Content enrichment — scrapes article body when NewsData content is missing."""

import logging

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

_SCRAPE_TIMEOUT = 10          # seconds
_MIN_CONTENT_LEN = 100        # treat content shorter than this as missing
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}


def _scrape_url(url: str) -> str | None:
    """
    Fetch the page at `url` and extract readable article text.
    Strategy:
      1. Look for <article> or <main> semantic containers.
      2. Collect all <p> tags inside; fall back to all <p> on the page.
      3. Return joined text, or None if nothing useful was found.
    """
    try:
        response = requests.get(url, headers=_HEADERS, timeout=_SCRAPE_TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as exc:
        logger.debug("Scrape failed [url=%s]: %s", url, exc)
        return None

    soup = BeautifulSoup(response.text, "lxml")

    # Remove noise tags
    for tag in soup(["script", "style", "nav", "footer", "aside", "form"]):
        tag.decompose()

    # Prefer semantic containers
    container = soup.find("article") or soup.find("main")
    source = container if container else soup

    paragraphs = [p.get_text(separator=" ", strip=True) for p in source.find_all("p")]
    text = " ".join(p for p in paragraphs if len(p) > 40)  # skip stub paragraphs

    return text if len(text) >= _MIN_CONTENT_LEN else None


def resolve_content(raw: dict) -> str | None:
    """
    3-tier content resolution for a raw NewsData article dict.

    Tier 1 — API content   : use if len > MIN_CONTENT_LEN
    Tier 2 — Scrape URL    : fetch the article page and extract body text
    Tier 3 — Description   : fall back to the description/preview field
    Returns None only if all three tiers fail (title used at embed time).
    """
    # Tier 1: API-provided content
    api_content = (raw.get("content") or "").strip()
    if len(api_content) >= _MIN_CONTENT_LEN:
        return api_content

    # Tier 2: scrape from source URL
    url = raw.get("link")
    if url:
        scraped = _scrape_url(url)
        if scraped:
            logger.debug("Scraped content from %s (%d chars)", url, len(scraped))
            return scraped

    # Tier 3: description as last resort
    description = (raw.get("description") or "").strip()
    return description or None
