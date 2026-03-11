"""APScheduler background task scheduler — runs scraping and digest jobs."""

# TODO: Import BackgroundScheduler from apscheduler.schedulers.background
# TODO: Import NewsFetcher, Embedder, DigestBuilder
# TODO: Import settings from app.core.config
# TODO: Import SessionLocal from app.db.session


def run_scrape_job():
    """
    Scheduled job — runs every SCRAPE_INTERVAL_HOURS hours.
    Pipeline:
      1. NewsFetcher.fetch_all() → raw article dicts
      2. Cleaner.is_valid() → discard invalid records
      3. Deduplicator.filter_new() → skip already-stored articles
      4. Insert new articles into DB
      5. Embedder.embed_batch() → compute embeddings for new articles
      6. Summarizer.summarize_batch() (async, non-blocking) → store summaries
    """
    # TODO: implement
    raise NotImplementedError


def start_scheduler():
    """
    Instantiate and start the APScheduler.
    Add run_scrape_job with an IntervalTrigger(hours=SCRAPE_INTERVAL_HOURS).
    Return the scheduler instance (called from app startup).
    """
    # TODO: scheduler = BackgroundScheduler()
    # TODO: scheduler.add_job(run_scrape_job, "interval", hours=settings.SCRAPE_INTERVAL_HOURS)
    # TODO: scheduler.start()
    # TODO: return scheduler
    raise NotImplementedError


def stop_scheduler(scheduler):
    """Gracefully shut down the scheduler (called from app shutdown)."""
    # TODO: scheduler.shutdown(wait=False)
    raise NotImplementedError
