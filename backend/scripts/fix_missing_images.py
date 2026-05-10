"""Replace NULL or empty image_url in existing articles with the placeholder.

Run from the backend/ directory:
    python scripts/fix_missing_images.py
"""

import logging
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.models.news import News
from app.services.image_constants import PLACEHOLDER_IMAGE_URL

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def main():
    db = SessionLocal()
    try:
        affected = (
            db.query(News)
            .filter((News.image_url == None) | (News.image_url == ""))
            .update({"image_url": PLACEHOLDER_IMAGE_URL}, synchronize_session=False)
        )
        db.commit()
        logger.info("Updated %d articles with placeholder image.", affected)
    finally:
        db.close()


if __name__ == "__main__":
    main()
