"""Remove semantically duplicate articles from the database.

Keeps the oldest article (lowest article_id) when duplicates are found.
Dry-run by default — pass --delete to actually remove rows.

Run from the backend/ directory:
    python scripts/dedup_existing.py           # dry run
    python scripts/dedup_existing.py --delete  # actually delete
"""

import logging
import sys
import os

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.models.news import News
from app.recommender.dedup import SIMILARITY_THRESHOLD

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def find_duplicates(db) -> list[int]:
    """
    Load all articles with embeddings, sorted by article_id (oldest first).
    Iterate in order: each article is checked against all previously accepted
    articles. If similarity >= threshold, mark it for deletion.
    Returns a list of article_ids to delete.
    """
    rows = (
        db.query(News.article_id, News.title, News.embedding)
        .filter(News.embedding.isnot(None))
        .order_by(News.article_id.asc())
        .all()
    )

    if not rows:
        logger.info("No articles with embeddings found.")
        return []

    logger.info("Loaded %d articles with embeddings", len(rows))

    ids = [r.article_id for r in rows]
    titles = [r.title for r in rows]
    mat = np.array([r.embedding for r in rows], dtype=np.float32)
    norms = np.linalg.norm(mat, axis=1, keepdims=True) + 1e-10
    mat = mat / norms  # normalize once

    to_delete: list[int] = []
    kept_indices: list[int] = []   # indices of articles we're keeping
    kept_mat = np.empty((0, mat.shape[1]), dtype=np.float32)

    for i, (aid, title) in enumerate(zip(ids, titles)):
        if kept_mat.shape[0] == 0:
            kept_indices.append(i)
            kept_mat = mat[i][np.newaxis]
            continue

        sims = kept_mat @ mat[i]
        max_sim = float(sims.max())

        if max_sim >= SIMILARITY_THRESHOLD:
            best_match_idx = kept_indices[int(sims.argmax())]
            logger.info(
                "  DUPLICATE (sim=%.3f): [%d] %s  ←→  [%d] %s",
                max_sim,
                ids[best_match_idx], titles[best_match_idx][:50],
                aid, title[:50],
            )
            to_delete.append(aid)
        else:
            kept_indices.append(i)
            kept_mat = np.vstack([kept_mat, mat[i]])

    return to_delete


def main():
    dry_run = "--delete" not in sys.argv

    db = SessionLocal()
    try:
        to_delete = find_duplicates(db)

        if not to_delete:
            logger.info("No duplicates found.")
            return

        logger.info("\nFound %d duplicate articles to remove", len(to_delete))

        if dry_run:
            logger.info("DRY RUN — run with --delete to actually remove them")
            return

        deleted = db.query(News).filter(News.article_id.in_(to_delete)).delete(synchronize_session=False)
        db.commit()
        logger.info("Deleted %d articles.", deleted)

    finally:
        db.close()


if __name__ == "__main__":
    main()
