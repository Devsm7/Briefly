"""Check every article's image_url and replace broken ones with the placeholder.

Run from the backend/ directory:
    python scripts/fix_broken_images.py
"""

import logging
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.models.news import News
from app.services.image_constants import PLACEHOLDER_IMAGE_URL
from app.services.image_validator import is_valid_image_url

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

WORKERS = 20  # concurrent HTTP checks


def main():
    db = SessionLocal()
    try:
        rows = (
            db.query(News.article_id, News.image_url)
            .filter(News.image_url != None, News.image_url != PLACEHOLDER_IMAGE_URL)
            .all()
        )
        total = len(rows)
        logger.info("Checking %d article image URLs with %d workers...", total, WORKERS)

        broken_ids: list[int] = []

        with ThreadPoolExecutor(max_workers=WORKERS) as pool:
            futures = {pool.submit(is_valid_image_url, row.image_url): row.article_id for row in rows}
            done = 0
            for future in as_completed(futures):
                article_id = futures[future]
                done += 1
                if not future.result():
                    broken_ids.append(article_id)
                if done % 50 == 0 or done == total:
                    logger.info("  progress: %d/%d checked, %d broken so far", done, total, len(broken_ids))

        logger.info("Found %d broken image URLs", len(broken_ids))

        if broken_ids:
            db.query(News).filter(News.article_id.in_(broken_ids)).update(
                {"image_url": PLACEHOLDER_IMAGE_URL}, synchronize_session=False
            )
            db.commit()
            logger.info("Replaced %d broken images with placeholder.", len(broken_ids))
        else:
            logger.info("All images are valid — nothing to update.")

    finally:
        db.close()


if __name__ == "__main__":
    main()
