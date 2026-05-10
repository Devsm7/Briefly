"""Semantic duplicate detection using cosine similarity on summary embeddings."""

import numpy as np
from sqlalchemy.orm import Session

from app.models.news import News

SIMILARITY_THRESHOLD = 0.92


def load_existing_embeddings(db: Session) -> np.ndarray:
    """Load and normalize all existing article embeddings from the DB into a matrix."""
    rows = db.query(News.embedding).filter(News.embedding.isnot(None)).all()
    if not rows:
        return np.empty((0,), dtype=np.float32)
    mat = np.array([r[0] for r in rows], dtype=np.float32)
    norms = np.linalg.norm(mat, axis=1, keepdims=True) + 1e-10
    return mat / norms


def is_near_duplicate(new_emb: list[float], existing_embs: np.ndarray) -> tuple[bool, float]:
    """
    Check if new_emb is semantically too close to any existing embedding.
    Returns (is_duplicate, max_similarity).
    """
    if existing_embs.ndim == 1 and existing_embs.shape[0] == 0:
        return False, 0.0
    a = np.array(new_emb, dtype=np.float32)
    a = a / (np.linalg.norm(a) + 1e-10)
    sims = existing_embs @ a
    max_sim = float(sims.max())
    return max_sim >= SIMILARITY_THRESHOLD, max_sim


def add_to_matrix(emb: list[float], existing_embs: np.ndarray) -> np.ndarray:
    """Normalize and append a new embedding to the in-memory matrix."""
    row = np.array(emb, dtype=np.float32)
    row = row / (np.linalg.norm(row) + 1e-10)
    if existing_embs.ndim == 1 and existing_embs.shape[0] == 0:
        return row[np.newaxis]
    return np.vstack([existing_embs, row])
