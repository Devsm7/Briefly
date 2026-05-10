"""APScheduler background task scheduler — runs the daily news scrape job."""

import logging
from datetime import datetime, timedelta

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.news import News
from app.recommender.dedup import add_to_matrix, is_near_duplicate, load_existing_embeddings
from app.recommender.embedder import embedder
from app.services.content_enricher import resolve_content
from app.services.image_validator import resolve_image_url
from app.services.newsdata_service import NewsdataService, _CATEGORY_MAP
from app.services.summarizer import generate_summary, translate_to_arabic

logger = logging.getLogger(__name__)


def run_scrape_job():
    """Fetch all categories from NewsData.io and upsert into DB."""
    db = SessionLocal()
    try:
        service = NewsdataService()
        raw_articles = service.fetch_all_categories()
        inserted = service.upsert_articles(db, raw_articles)
        logger.info("Scrape job complete: %d new articles inserted", inserted)
    except Exception:
        logger.exception("Scrape job failed")
    finally:
        db.close()


def run_embed_job():
    """Embed any articles that have a summary but no embedding vector."""
    db = SessionLocal()
    try:
        articles = db.query(News).filter(
            News.embedding == None,
            News.summary != None
        ).all()
        if articles:
            texts = [a.summary for a in articles]
            vectors = embedder.embed_batch(texts)
            for article, vec in zip(articles, vectors):
                article.embedding = vec
            db.commit()
        logger.info("Embed job complete: %d articles embedded", len(articles))
    except Exception:
        logger.exception("Embed job failed")
    finally:
        db.close()


def run_arabic_fetch_job():
    """Fetch Arabic-language news and upsert into DB — runs every hour."""
    logger.info("Arabic fetch job started")
    db = SessionLocal()
    try:
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
            logger.error("NewsData API error: %s", data)
            return
        raw_articles = data.get("results") or []
        logger.info("Arabic fetch: got %d articles from API", len(raw_articles))

        existing_ids = {r[0] for r in db.query(News.newsdata_id).filter(News.newsdata_id.isnot(None)).all()}
        existing_urls = {r[0] for r in db.query(News.url).filter(News.url.isnot(None)).all()}
        existing_embs = load_existing_embeddings(db)

        inserted = skipped = 0
        for raw in raw_articles:
            nid = raw.get("article_id")
            url = raw.get("link")

            if (nid and nid in existing_ids) or (url and url in existing_urls):
                skipped += 1
                continue

            creators = raw.get("creator") or []
            categories = raw.get("category") or []
            raw_cat = categories[0] if categories else None
            article = News(
                newsdata_id=nid,
                title=(raw.get("title") or "").strip(),
                description=(raw.get("description") or "").strip() or None,
                content=resolve_content(raw),
                url=url,
                image_url=resolve_image_url(raw.get("image_url")),
                published_date=raw.get("pubDate"),
                source=raw.get("source_id"),
                category=_CATEGORY_MAP.get(raw_cat, raw_cat),
                language="ar",
                keywords=raw.get("keywords") or [],
                author=", ".join(creators) if creators else None,
            )

            if not article.title or not article.content:
                skipped += 1
                continue

            db.add(article)
            db.flush()

            article.summary = generate_summary(article.content, article.title)
            if not article.summary:
                db.rollback()
                skipped += 1
                continue

            article.summary_ar = translate_to_arabic(article.summary)

            emb = embedder.embed_text(article.summary)
            duplicate, sim = is_near_duplicate(emb, existing_embs)
            if duplicate:
                db.rollback()
                logger.info("Arabic fetch: skip duplicate (sim=%.3f): %s", sim, article.title[:60])
                skipped += 1
                continue

            article.embedding = emb
            existing_embs = add_to_matrix(emb, existing_embs)
            if nid:
                existing_ids.add(nid)
            if url:
                existing_urls.add(url)
            inserted += 1

        db.commit()
        logger.info("Arabic fetch job done: inserted=%d skipped=%d", inserted, skipped)
    except Exception:
        logger.exception("Arabic fetch job failed")
        db.rollback()
    finally:
        db.close()


def start_scheduler():
    """Start APScheduler and return the instance (called from app startup)."""
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        run_scrape_job,
        IntervalTrigger(hours=settings.SCRAPE_INTERVAL_HOURS),
        next_run_time=datetime.now(),
    )
    scheduler.add_job(
        run_arabic_fetch_job,
        IntervalTrigger(hours=1),
        next_run_time=datetime.now() + timedelta(minutes=5),  # stagger after main scrape
    )
    scheduler.start()
    logger.info("Scheduler started — scrape every %dh, Arabic fetch every 1h", settings.SCRAPE_INTERVAL_HOURS)
    return scheduler


def stop_scheduler(scheduler):
    """Gracefully shut down the scheduler (called from app shutdown)."""
    scheduler.shutdown(wait=False)
    logger.info("Scheduler stopped")
