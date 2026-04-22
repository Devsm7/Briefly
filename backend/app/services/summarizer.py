"""Ollama-powered article summarization."""

import logging

import requests

from app.core.config import settings

logger = logging.getLogger(__name__)

_SUMMARY_TIMEOUT = 120  # seconds


def generate_summary(content: str | None, title: str) -> str | None:
    """
    Generate a 2-3 sentence summary of an article using Ollama mistral.

    Args:
        content: The article body text (may be None or short).
        title: The article title, used as context.

    Returns:
        The generated summary string, or None if summarization failed.
    """
    if not content or len(content) < 50:
        return None

    # Truncate to avoid excessively long prompts (Ollama context limits vary)
    truncated = content[:4000]

    prompt = f"""Summarize the following article in 2-3 concise sentences.
Give the reader a clear sense of what the article is about without editorializing.

Title: {title}

Article:
{truncated}

Summary:"""

    try:
        resp = requests.post(
            f"{settings.OLLAMA_BASE_URL}/api/generate",
            json={
                "model": settings.OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.3, "num_predict": 256},
            },
            timeout=_SUMMARY_TIMEOUT,
        )
        resp.raise_for_status()
        result = resp.json()
        summary = (result.get("response") or "").strip()
        if summary:
            logger.debug("Generated summary (%d chars) for title: %s", len(summary), title)
            return summary
        return None
    except requests.RequestException as exc:
        logger.warning("Ollama summarization failed: %s", exc)
        return None
    except Exception as exc:
        logger.warning("Unexpected error during summarization: %s", exc)
        return None
