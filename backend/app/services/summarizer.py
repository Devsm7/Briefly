"""Ollama-powered article summarization."""

import logging

import requests

from app.core.config import settings

logger = logging.getLogger(__name__)

_SUMMARY_TIMEOUT = 240  # seconds


def generate_summary(content: str | None, title: str, retries: int = 2) -> str | None:
    """
    Generate a 2-3 sentence summary of an article using Ollama mistral.

    Returns the generated summary string, or None if summarization failed.
    """
    if not content or len(content) < 50:
        return None

    truncated = content[:4000]

    prompt = f"""Summarize this article in 2-3 concise sentences.
Give the reader a clear sense of what the article is about without editorializing.

Title: {title}

Article:
{truncated}

Summary:"""

    url = f"{settings.OLLAMA_BASE_URL}/api/generate"

    for attempt in range(retries + 1):
        try:
            response = requests.post(
                url,
                json={
                    "model": settings.OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.3, "num_predict": 256},
                },
                timeout=_SUMMARY_TIMEOUT,
            )
            response.raise_for_status()
            data = response.json()
            summary = (data.get("response") or "").strip()
            if summary:
                logger.debug("Generated summary (%d chars) for: %s", len(summary), title)
                return summary
            if attempt == retries:
                return None
        except requests.Timeout:
            logger.warning("Ollama summarization timed out after %ds", _SUMMARY_TIMEOUT)
            if attempt == retries:
                return None
        except Exception as exc:
            logger.warning("Unexpected error during summarization: %s", exc)
            if attempt == retries:
                return None


def generate_category_summary(articles: list[dict], category: str) -> str | None:
    """
    Generate a single overall summary for all articles in a category.
    Builds a digest prompt from article titles and summaries, asks for
    a concise paragraph covering the key themes and highlights.
    """
    if not articles:
        return None

    items = []
    for a in articles:
        title = a.get("title", "")
        preview = a.get("preview") or a.get("description") or ""
        items.append(f"- {title}: {preview[:200]}")

    context = "\n".join(items[:20])

    prompt = f"""You are a news digest writer. Given the following articles in the {category} category,
write a concise 2-3 paragraph overview that captures the key themes, major developments,
and why they matter. Write in a neutral, informative tone. Do not just list articles —
synthesize them into a coherent summary.

Articles:
{context}

Digest:"""

    url = f"{settings.OLLAMA_BASE_URL}/api/generate"

    for attempt in range(2):
        try:
            response = requests.post(
                url,
                json={
                    "model": settings.OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.3, "num_predict": 350},
                },
                timeout=_SUMMARY_TIMEOUT,
            )
            response.raise_for_status()
            data = response.json()
            digest = (data.get("response") or "").strip()
            if digest:
                logger.debug("Generated category digest for %s (%d chars)", category, len(digest))
                return digest
            if attempt == 1:
                return None
        except Exception as exc:
            logger.warning("Category digest generation failed: %s", exc)
            if attempt == 1:
                return None
