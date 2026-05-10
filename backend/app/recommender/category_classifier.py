"""LLM-based category classifier using Ollama (Mistral).

Asks the model to pick the best category from a fixed list given the article
title and summary. Falls back to 'Other' if the model returns an unrecognised
label or if the request fails.
"""

import logging
import re

import requests

from app.core.config import settings

logger = logging.getLogger(__name__)

VALID_CATEGORIES = {
    "business", "sport", "politics", "tech", "health",
    "entertainment", "world", "environment", "food", "tourism",
}

_PROMPT_TEMPLATE = """You are a news article classifier. Given a title and summary, respond with exactly one category from this list:
business, sport, politics, tech, health, entertainment, world, environment, food, tourism, Other

Rules:
- Respond with ONLY the category word, nothing else.
- Use 'Other' only if the article clearly does not fit any category.

Title: {title}
Summary: {summary}

Category:"""


def classify_with_llm(title: str, summary: str) -> str:
    """Ask Mistral to classify the article. Returns a valid category or 'Other'."""
    prompt = _PROMPT_TEMPLATE.format(title=title[:200], summary=summary[:500])

    try:
        resp = requests.post(
            f"{settings.OLLAMA_BASE_URL}/api/generate",
            json={
                "model": settings.OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.0, "num_predict": 10},
            },
            timeout=30,
        )
        resp.raise_for_status()
        raw = (resp.json().get("response") or "").strip().lower()
        # Extract the first word in case the model adds punctuation
        word = re.split(r"[\s,.\n]", raw)[0]
        if word in VALID_CATEGORIES:
            return word
        if word == "other":
            return "Other"
        logger.warning("LLM returned unrecognised category '%s' — using Other", raw)
        return "Other"
    except Exception as exc:
        logger.warning("Category classification failed: %s", exc)
        return "Other"


def classify(embedding: list[float], title: str = "", summary: str = "") -> str:
    """
    Classify an article into a category using the LLM.
    `embedding` kept in signature for API compatibility but not used.
    Falls back to 'Other' on any failure.
    """
    if not title and not summary:
        return "Other"
    return classify_with_llm(title, summary)
