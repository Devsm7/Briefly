"""APScheduler background task scheduler — runs the daily news scrape job."""

import logging
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.news import News
from app.recommender.embedder import embedder
from app.services.newsdata_service import NewsdataService

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


def start_scheduler():
    """Start APScheduler and return the instance (called from app startup)."""
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        run_scrape_job,
        IntervalTrigger(hours=settings.SCRAPE_INTERVAL_HOURS),
        next_run_time=datetime.now(),   # run immediately on startup
    )
    scheduler.start()
    logger.info("Scheduler started — runs every %dh", settings.SCRAPE_INTERVAL_HOURS)
    return scheduler


def stop_scheduler(scheduler):
    """Gracefully shut down the scheduler (called from app shutdown)."""
    scheduler.shutdown(wait=False)
    logger.info("Scheduler stopped")
