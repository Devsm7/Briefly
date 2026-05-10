"""Fetch May 2026 news from NewsData.io archive and upsert into the database.

Run from the backend/ directory:
    python scripts/fetch_may_news.py
"""

import logging
import sys
import os
import time

import requests

# Allow imports from backend/app/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.news import News
from app.recommender.dedup import add_to_matrix, is_near_duplicate, load_existing_embeddings
from app.recommender.embedder import embedder
from app.services.content_enricher import resolve_content
from app.services.image_validator import resolve_image_url
from app.services.newsdata_service import _CATEGORY_MAP, _DEFAULT_CATEGORIES
from app.services.summarizer import generate_summary

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

LANGUAGES = "en,ar"
COUNTRIES = "sa,us"
MAX_PAGES_PER_CATEGORY = 5
PAGE_DELAY_SECONDS = 2        # between pages within a category
CATEGORY_DELAY_SECONDS = 10   # between categories


def fetch_latest_category(api_key: str, category: str) -> list[dict]:
    """Fetch latest articles for one category."""
    results: list[dict] = []
    next_page: str | None = None

    for page_num in range(MAX_PAGES_PER_CATEGORY):
        params: dict = {
            "apikey": api_key,
            "category": category,
            "language": LANGUAGES,
            "country": COUNTRIES,
            "image": 1,
            "video": 0,
            "removeduplicate": 1,
        }
        if next_page:
            params["page"] = next_page

        try:
            resp = requests.get(
                f"{settings.NEWSDATA_BASE_URL}/latest",
                params=params,
                timeout=20,
            )
            if resp.status_code == 429:
                retry_after = int(resp.headers.get("Retry-After", 60))
                logger.warning("Rate limited — waiting %ds before retry", retry_after)
                time.sleep(retry_after)
                # retry once
                resp = requests.get(
                    f"{settings.NEWSDATA_BASE_URL}/latest",
                    params=params,
                    timeout=20,
                )
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as exc:
            logger.error("Latest fetch failed [category=%s page=%d]: %s", category, page_num, exc)
            break

        if data.get("status") != "success":
            logger.error("NewsData error [category=%s]: %s", category, data)
            break

        page_results = data.get("results") or []
        results.extend(page_results)
        logger.info("  category=%-12s  page=%d  fetched=%d", category, page_num + 1, len(page_results))

        next_page = data.get("nextPage")
        if not next_page:
            break

        time.sleep(PAGE_DELAY_SECONDS)

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
        "language": (raw.get("language") or "en").lower(),
        "keywords": raw.get("keywords") or [],
        "author": author,
    }


def upsert(db, raw_articles: list[dict]) -> tuple[int, int]:
    existing_ids: set[str] = {
        r[0] for r in db.query(News.newsdata_id).filter(News.newsdata_id.isnot(None)).all()
    }
    existing_urls: set[str] = {
        r[0] for r in db.query(News.url).filter(News.url.isnot(None)).all()
    }

    existing_embs = load_existing_embeddings(db)
    logger.info("Loaded %d existing embeddings for semantic dedup", existing_embs.shape[0])

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

        emb = embedder.embed_text(article.summary)

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

        if inserted % 20 == 0:
            db.commit()
            logger.info("  -- committed %d so far --", inserted)

    db.commit()
    return inserted, skipped


def main():
    api_key = settings.NEWSDATA_API_KEY
    if not api_key:
        logger.error("NEWSDATA_API_KEY is not set in .env")
        sys.exit(1)

    logger.info("Fetching latest news (country=%s, language=%s)", COUNTRIES, LANGUAGES)

    all_raw: list[dict] = []
    for i, cat in enumerate(_DEFAULT_CATEGORIES):
        if i > 0:
            logger.info("Waiting %ds before next category...", CATEGORY_DELAY_SECONDS)
            time.sleep(CATEGORY_DELAY_SECONDS)
        logger.info("Fetching category: %s", cat)
        raw = fetch_latest_category(api_key, cat)
        logger.info("  total fetched for %s: %d", cat, len(raw))
        all_raw.extend(raw)

    logger.info("\nTotal raw articles fetched: %d", len(all_raw))
    logger.info("Upserting into database (summarize + embed)...")

    db = SessionLocal()
    try:
        inserted, skipped = upsert(db, all_raw)
    finally:
        db.close()

    logger.info("\nDone. inserted=%d  skipped=%d", inserted, skipped)


if __name__ == "__main__":
    main()
