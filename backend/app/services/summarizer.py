"""Article summarization — Ollama for per-article summaries, Groq for translation and overall brief."""

import logging

import requests
from openai import OpenAI as _OpenAI

from app.core.config import settings

logger = logging.getLogger(__name__)

_SUMMARY_TIMEOUT = 240  # seconds — used by Ollama calls
_GROQ_MODEL = "llama-3.3-70b-versatile"

# Maps category name → the answers key holding its topic selections
_TOPIC_QUESTION: dict[str, str] = {
    "tech": "Q04", "politics": "Q07", "sport": "Q13",
    "business": "Q15", "health": "Q19", "science": "Q22",
}

# Human-readable labels for survey topic codes
_TOPIC_LABELS: dict[str, dict[str, str]] = {
    "tech": {
        "ai": "AI & Machine Learning", "cybersecurity": "Cybersecurity",
        "startups": "Startups & Venture Capital", "electronics": "Consumer Electronics",
        "software": "Software & Apps", "science": "Science & Space",
    },
    "politics": {
        "domestic": "Domestic Politics", "international": "International Relations",
        "elections": "Elections", "economic": "Economic Policy",
        "social": "Social Policy", "environment": "Environmental Policy",
    },
    "sport": {
        "football": "Football", "basketball": "Basketball", "f1": "Formula 1",
        "tennis": "Tennis", "cricket": "Cricket", "athletics": "Athletics",
        "rugby": "Rugby", "baseball": "Baseball",
    },
    "business": {
        "markets": "Financial Markets", "crypto": "Cryptocurrency",
        "entrepreneurship": "Entrepreneurship", "real_estate": "Real Estate",
        "personal_finance": "Personal Finance", "economy": "Global Economy",
    },
    "health": {
        "mental_health": "Mental Health", "nutrition": "Nutrition",
        "fitness": "Fitness & Exercise", "medical_research": "Medical Research",
        "public_health": "Public Health", "longevity": "Longevity",
    },
    "science": {
        "space": "Space & Astronomy", "physics": "Physics", "biology": "Biology",
        "climate": "Climate Science", "tech_science": "Emerging Technology",
        "archaeology": "Archaeology",
    },
}


def _groq_client() -> _OpenAI:
    return _OpenAI(
        api_key=settings.GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1",
    )


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


def translate_to_arabic(text: str) -> str | None:
    """Translate English text to Arabic using Google Translate (unofficial free endpoint)."""
    if not text or len(text) < 5:
        return None
    try:
        # Split into ≤4000-char chunks to stay within URL limits
        chunks = [text[i:i + 4000] for i in range(0, len(text), 4000)]
        parts = []
        for chunk in chunks:
            resp = requests.get(
                "https://translate.googleapis.com/translate_a/single",
                params={"client": "gtx", "sl": "en", "tl": "ar", "dt": "t", "q": chunk},
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()
            parts.append("".join(seg[0] for seg in data[0] if seg[0]))
        result = "".join(parts).strip()
        return result or None
    except Exception as exc:
        logger.warning("Translation failed: %s", exc)
        return None


def generate_overall_summary(db, interest_vector: dict | None = None, limit: int = 100) -> str | None:
    """
    Generate a personalized news brief in English using Groq.
    If interest_vector is provided, articles are sorted by the user's category interest scores
    so the brief leads with the topics the user cares most about.
    """
    from app.models.news import News

    articles = db.query(News).filter(
        News.summary.isnot(None),
    ).order_by(News.created_at.desc()).limit(limit).all()

    if len(articles) < 2:
        return None

    if interest_vector:
        # Sort articles by the user's interest score for their category (desc), recency as tiebreak
        def _interest(a):
            cat = (a.category or "other").lower().strip()
            return interest_vector.get(cat, 0.0)
        articles = sorted(articles, key=_interest, reverse=True)

        # Build prompt sections per category in interest order
        seen_cats: list[str] = []
        by_cat: dict[str, list] = {}
        for a in articles:
            cat = (a.category or "other").lower().strip()
            if cat not in by_cat:
                by_cat[cat] = []
                seen_cats.append(cat)
            by_cat[cat].append(a)

        sections: list[str] = []
        for cat in seen_cats[:6]:  # top 6 categories
            score = interest_vector.get(cat, 0.0)
            n = max(2, round(score * 5))  # 5 articles for score=1.0, 2 for score=0.4
            cat_articles = by_cat[cat][:n]
            lines = [f"  - {a.title}: {(a.summary or '')[:120]}" for a in cat_articles]
            sections.append(f"[{cat.capitalize()} — interest score {score:.1f}]\n" + "\n".join(lines))
        context = "\n\n".join(sections)

        prompt = (
            "You are a personalized news analyst. The sections below are ordered by the user's "
            "interest level (highest first). Write a 3-4 paragraph news brief in English only "
            "(absolutely no Arabic words). Lead with the highest-interest topics and give them "
            "more detail. Lower-interest topics may be briefly mentioned at the end. "
            "Synthesize — do not just list headlines.\n\n"
            f"{context}\n\nPersonalized News Brief:"
        )
    else:
        items = [f"- {a.title}: {(a.summary or '')[:150]}" for a in articles[:30]]
        context = "\n".join(items)
        prompt = (
            "You are a world news analyst. Review the following headlines and summaries "
            "and write a concise 2-3 paragraph brief in English only (no Arabic words). "
            "Cover the most important global themes. Synthesize — do not just list items.\n\n"
            f"Headlines & Summaries:\n{context}\n\nGlobal News Brief:"
        )

    try:
        client = _groq_client()
        resp = client.chat.completions.create(
            model=_GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=700,
        )
        digest = (resp.choices[0].message.content or "").strip()
        if digest:
            logger.debug("Generated overall summary (%d chars)", len(digest))
        return digest or None
    except Exception as exc:
        logger.warning("Overall summary generation failed: %s", exc)
        return None


def generate_user_interest_description(
    interest_vector: dict[str, float],
    answers: dict | None = None,
) -> str | None:
    """
    Generate a 1-2 sentence natural language description of a user's interests.
    Uses subcategory topic selections from `answers` for a specific, YouTube/X-style profile.
    Falls back to category-only description if answers are not provided.
    """
    if not interest_vector:
        return None

    sorted_cats = sorted(interest_vector.items(), key=lambda x: x[1], reverse=True)
    top_cats = [(cat, weight) for cat, weight in sorted_cats if weight > 0.1]

    if not top_cats:
        return None

    lines = []
    for cat, weight in top_cats:
        topic_codes = (answers or {}).get(_TOPIC_QUESTION.get(cat, ""), [])
        if isinstance(topic_codes, list):
            labels = [_TOPIC_LABELS.get(cat, {}).get(code, code) for code in topic_codes]
        else:
            labels = []
        topic_str = f": {', '.join(labels)}" if labels else ""
        lines.append(f"  - {cat} (interest {weight:.1f}){topic_str}")
    context = "\n".join(lines)

    prompt = f"""You are a user interest profiler. A user selected the following interest categories
and specific topics within each. Write a concise 1-2 sentence profile in third person.
Name the actual subtopics, not just the categories.

User interests:
{context}

User interest profile:"""

    try:
        client = _groq_client()
        resp = client.chat.completions.create(
            model=_GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=150,
        )
        description = (resp.choices[0].message.content or "").strip()
        if description:
            logger.debug("Generated interest description: %s", description)
        return description or None
    except Exception as exc:
        logger.warning("Interest description generation failed: %s", exc)
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
