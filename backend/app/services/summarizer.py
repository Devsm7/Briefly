"""Modular AI summarization service using Ollama."""

import logging
import re
from functools import lru_cache

import requests
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.news import News

logger = logging.getLogger(__name__)

# Simple in-memory cache (article_id -> summary)
_summary_cache: dict[int, str] = {}

# Prompt template for summarization
_SUMMARIZE_PROMPT = """Summarize the following article in 2-3 clear sentences.
Focus on the key facts and why it matters. Be concise and informative.

Article title: {title}
Article content: {content}

Summary:"""


def _call_ollama(prompt: str) -> str | None:
    """Call Ollama API and return the summary text, or None on failure."""
    try:
        response = requests.post(
            f"{settings.OLLAMA_BASE_URL}/api/generate",
            json={
                "model": settings.OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.3, "num_predict": 200},
            },
            timeout=30,
        )
        response.raise_for_status()
        result = response.json()
        text = result.get("response", "").strip()
        # Clean up any lingering thinking tags or artifacts
        text = re.sub(r"<\|.*?\|>", "", text).strip()
        return text if len(text) > 20 else None
    except requests.RequestException as exc:
        logger.warning("Ollama call failed: %s", exc)
        return None


def summarize_content(title: str, content: str) -> str | None:
    """
    Generate a 2-3 sentence AI summary for the given article.
    Returns None if summarization fails.
    """
    if not content or len(content.strip()) < 50:
        return None

    prompt = _SUMMARIZE_PROMPT.format(title=title[:200], content=content[:3000])
    return _call_ollama(prompt)


def get_ai_summary(db: Session, article_id: int, title: str, content: str) -> str:
    """
    Get or generate AI summary for an article with caching.

    Priority:
      1. Return cached summary from memory
      2. Return stored ai_summary from DB
      3. Generate new summary via Ollama
      4. Fall back to description if AI fails

    Stores newly generated summary in DB for future use.
    """
    # Check memory cache
    if article_id in _summary_cache:
        return _summary_cache[article_id]

    # Check DB cache
    article = db.query(News).filter(News.article_id == article_id).first()
    if article and article.ai_summary:
        _summary_cache[article_id] = article.ai_summary
        return article.ai_summary

    # Generate new summary
    summary = summarize_content(title, content or "")

    if summary:
        # Store in memory cache and DB
        _summary_cache[article_id] = summary
        if article:
            article.ai_summary = summary
            db.commit()
    else:
        # Fall back to description
        summary = article.description if article else None

    return summary or ""


def clear_cache():
    """Clear the in-memory summary cache."""
    _summary_cache.clear()