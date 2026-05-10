"""Backfill summary_ar for existing Arabic articles that have a summary but no translation.

Run from the backend/ directory:
    python scripts/backfill_summary_ar.py
"""

import logging
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.models.news import News
from app.services.summarizer import translate_to_arabic

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def get_pending_ids() -> list[int]:
    db = SessionLocal()
    try:
        return [
            r[0] for r in db.query(News.article_id)
            .filter(
                News.language == "ar",
                News.summary.isnot(None),
                News.summary_ar.is_(None),
            )
            .order_by(News.article_id)
            .all()
        ]
    finally:
        db.close()


def process_one(article_id: int) -> bool:
    """Open a fresh DB connection per article to avoid SSL idle-timeout drops."""
    db = SessionLocal()
    try:
        article = db.query(News).filter(News.article_id == article_id).first()
        if not article or not article.summary:
            return False
        translated = translate_to_arabic(article.summary)
        if not translated:
            return False
        article.summary_ar = translated
        db.commit()
        return True
    except Exception as exc:
        logger.warning("DB error on article %d: %s", article_id, exc)
        db.rollback()
        return False
    finally:
        db.close()


def main():
    ids = get_pending_ids()
    total = len(ids)
    logger.info("Found %d Arabic articles needing translation", total)

    success = failed = 0
    for i, art_id in enumerate(ids, 1):
        ok = process_one(art_id)
        if ok:
            success += 1
            logger.info("[%d/%d] translated article_id=%d", i, total, art_id)
        else:
            failed += 1
            logger.warning("[%d/%d] failed article_id=%d", i, total, art_id)

    logger.info("Done. success=%d  failed=%d", success, failed)


if __name__ == "__main__":
    main()
