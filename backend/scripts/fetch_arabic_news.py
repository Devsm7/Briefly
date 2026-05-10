"""Fetch Arabic-language news (single API call) and upsert into the database.

Run from the backend/ directory:
    python scripts/fetch_arabic_news.py
"""

import logging
import sys
import os

import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.news import News
from app.recommender.dedup import add_to_matrix, is_near_duplicate, load_existing_embeddings
from app.recommender.embedder import embedder
from app.services.content_enricher import resolve_content
from app.services.image_validator import resolve_image_url
from app.services.newsdata_service import _CATEGORY_MAP
from app.services.summarizer import generate_summary, translate_to_arabic

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def fetch_arabic() -> list[dict]:
    params = {
        "apikey": settings.NEWSDATA_API_KEY,
        "language": "ar",
        "country": "sa,us",
        "image": 1,
        "video": 0,
        "removeduplicate": 1,
    }
    resp = requests.get(f"{settings.NEWSDATA_BASE_URL}/latest", params=params, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    if data.get("status") != "success":
        raise RuntimeError(f"NewsData error: {data}")
    results = data.get("results") or []
    logger.info("Fetched %d Arabic articles", len(results))
    return results


def map_article(raw: dict) -> dict:
    creators = raw.get("creator") or []
    author = ", ".join(creators) if creators else None
    categories = raw.get("category") or []
    raw_cat = categories[0] if categories else None
    category = _CATEGORY_MAP.get(raw_cat, raw_cat)
    return {
        "newsdata_id": raw.get("article_id"),
        "title": (raw.get("title") or "").strip(),
        "description": (raw.get("description") or "").strip() or None,
        "content": resolve_content(raw),
        "url": raw.get("link"),
        "image_url": resolve_image_url(raw.get("image_url")),
        "published_date": raw.get("pubDate"),
        "source": raw.get("source_id"),
        "category": category,
        "language": "ar",
        "keywords": raw.get("keywords") or [],
        "author": author,
    }


def upsert(db, raw_articles: list[dict]) -> tuple[int, int]:
    existing_ids = {r[0] for r in db.query(News.newsdata_id).filter(News.newsdata_id.isnot(None)).all()}
    existing_urls = {r[0] for r in db.query(News.url).filter(News.url.isnot(None)).all()}

    existing_embs = load_existing_embeddings(db)
    logger.info("Loaded %d existing embeddings for duplicate check", existing_embs.shape[0])

    inserted = skipped = 0
    total = len(raw_articles)

    for i, raw in enumerate(raw_articles, 1):
        nid = raw.get("article_id")
        url = raw.get("link")

        if (nid and nid in existing_ids) or (url and url in existing_urls):
            skipped += 1
            continue

        kwargs = map_article(raw)
        if not kwargs["title"] or not kwargs["content"]:
            skipped += 1
            continue

        article = News(**kwargs)
        db.add(article)
        db.flush()

        article.summary = generate_summary(kwargs["content"], kwargs["title"])
        if not article.summary:
            db.rollback()
            logger.warning("  [%d/%d] skip (summarization failed): %s", i, total, kwargs["title"][:60])
            skipped += 1
            continue

        article.summary_ar = translate_to_arabic(article.summary)

        emb = embedder.embed_text(article.summary)

        # Semantic duplicate check
        duplicate, sim = is_near_duplicate(emb, existing_embs)
        if duplicate:
            db.rollback()
            logger.info("  [%d/%d] skip (duplicate sim=%.3f): %s", i, total, sim, kwargs["title"][:60])
            skipped += 1
            continue

        article.embedding = emb

        existing_embs = add_to_matrix(emb, existing_embs)

        if nid:
            existing_ids.add(nid)
        if url:
            existing_urls.add(url)

        inserted += 1
        logger.info("  [%d/%d] saved: %s", i, total, kwargs["title"][:70])

    db.commit()
    return inserted, skipped


def main():
    if not settings.NEWSDATA_API_KEY:
        logger.error("NEWSDATA_API_KEY is not set in .env")
        sys.exit(1)

    raw_articles = fetch_arabic()

    db = SessionLocal()
    try:
        inserted, skipped = upsert(db, raw_articles)
    finally:
        db.close()

    logger.info("Done. inserted=%d  skipped=%d", inserted, skipped)


if __name__ == "__main__":
    main()
