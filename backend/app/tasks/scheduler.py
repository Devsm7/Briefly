"""APScheduler background task scheduler — runs the daily news scrape job."""

import logging
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.core.config import settings
from app.db.session import SessionLocal
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
