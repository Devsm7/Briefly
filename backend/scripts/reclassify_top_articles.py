"""Reclassify articles with category='Other' or 'top' using Ollama/Mistral.

Run from the backend/ directory:
    python scripts/reclassify_top_articles.py
"""

import logging
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.models.news import News
from app.recommender.category_classifier import classify_with_llm

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def main():
    db = SessionLocal()
    try:
        rows = (
            db.query(News)
            .filter(News.category.in_(["top", "Other"]), News.summary.isnot(None))
            .all()
        )
        total = len(rows)
        logger.info("Found %d articles to reclassify (category='top' or 'Other')", total)

        counts: dict[str, int] = {}
        for i, article in enumerate(rows, 1):
            new_cat = classify_with_llm(article.title or "", article.summary or "")
            article.category = new_cat
            counts[new_cat] = counts.get(new_cat, 0) + 1
            logger.info("  [%d/%d] %-15s ← %s", i, total, new_cat, (article.title or "")[:60])

            if i % 20 == 0:
                db.commit()
                logger.info("  -- committed %d --", i)

        db.commit()

        logger.info("\nDone. Distribution:")
        for cat, cnt in sorted(counts.items(), key=lambda x: -x[1]):
            logger.info("  %-15s %d", cat, cnt)

    finally:
        db.close()


if __name__ == "__main__":
    main()
