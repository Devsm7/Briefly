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
