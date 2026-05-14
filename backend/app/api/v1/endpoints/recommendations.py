"""Personalized recommendation endpoints."""

import logging
import time

import numpy as np
from fastapi import APIRouter, Depends, HTTPException

# ── In-process recommendations cache ─────────────────────────────────────────
# Key: user_id  Value: (timestamp, list[article_dict])
# Invalidated on like/dislike (via invalidate_recs_cache) and on survey change
# (frontend clears recommendations_cache session key which forces a re-fetch).
_recs_cache: dict[int, tuple[float, list]] = {}
_RECS_TTL = 300  # 5 minutes


def _get_recs_cache(user_id: int) -> list | None:
    entry = _recs_cache.get(user_id)
    if entry and time.time() - entry[0] < _RECS_TTL:
        return entry[1]
    return None


def _set_recs_cache(user_id: int, articles: list) -> None:
    _recs_cache[user_id] = (time.time(), articles)


def invalidate_recs_cache(user_id: int) -> None:
    _recs_cache.pop(user_id, None)

from app.api.deps import get_current_user, get_db
from app.models.news import News
from app.models.survey import SurveyPreference
from app.models.user import User
from app.models.user_interaction import UserInteraction
from app.recommender.ranker import Ranker
from app.services.news_service import _TOPIC_SEARCH_TERMS, article_to_dict, build_user_embedding_from_categories
from app.services.summarizer import _TOPIC_QUESTION
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/recommendations", tags=["recommendations"])
ranker = Ranker()


def _selected_topic_keywords(survey) -> list[str]:
    """Collect all keyword terms for the subtopics the user explicitly selected in the survey."""
    if not survey or not survey.answers:
        return []
    terms: list[str] = []
    for cat in (survey.categories or []):
        q_key = _TOPIC_QUESTION.get(cat, "")
        codes = survey.answers.get(q_key, [])
        if isinstance(codes, list):
            for code in codes:
                terms.extend(_TOPIC_SEARCH_TERMS.get(code, []))
    return terms


@router.get("")
def get_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    page: int = 1,
    per_page: int = 50,
):
    """
    GET /recommendations — Return paginated personalized articles for the current user.

    Query params:
      page     — page number, 1-indexed (default 1)
      per_page — articles per page (default 50, max 100)
    """
    if page < 1:
        raise HTTPException(status_code=400, detail="page must be >= 1")
    if per_page < 1 or per_page > 1000:
        raise HTTPException(status_code=400, detail="per_page must be between 1 and 1000")

    # ── Cache hit — skip DB ranking entirely ─────────────────────────────────
    cached = _get_recs_cache(current_user.id)
    if cached is not None:
        total = len(cached)
        offset = (page - 1) * per_page
        return {
            "articles": cached[offset:offset + per_page],
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page or 1,
        }

    survey = db.query(SurveyPreference).filter(
        SurveyPreference.user_id == current_user.id
    ).first()
    interest_vector = survey.interest_vector if survey else {}

    liked_ids = [
        r.article_id for r in
        db.query(UserInteraction.article_id)
        .filter(UserInteraction.user_id == current_user.id, UserInteraction.action == "like")
        .all()
    ]
    disliked_ids = [
        r.article_id for r in
        db.query(UserInteraction.article_id)
        .filter(UserInteraction.user_id == current_user.id, UserInteraction.action == "dislike")
        .all()
    ]

    liked_embeddings = [
        r.embedding for r in
        db.query(News.embedding)
        .filter(News.article_id.in_(liked_ids), News.embedding != None)
        .all()
    ] if liked_ids else []

    disliked_embeddings = [
        r.embedding for r in
        db.query(News.embedding)
        .filter(News.article_id.in_(disliked_ids), News.embedding != None)
        .all()
    ] if disliked_ids else []

    topic_keywords = _selected_topic_keywords(survey)

    # Fallback — no likes yet: rank all articles by survey interest_vector
    if not liked_embeddings:
        all_articles = db.query(News).filter(News.summary.isnot(None)).all()

        if survey and survey.user_embedding is not None:
            user_emb = survey.user_embedding  # cache hit
        else:
            # Build from existing article embeddings — topic-aware, no Groq call
            answers = survey.answers if survey else {}
            user_emb = build_user_embedding_from_categories(db, interest_vector, answers=answers)
            if survey and user_emb:
                survey.user_embedding = user_emb
                db.commit()

        ranked = ranker.rank_articles(
            all_articles,
            user_embedding=user_emb,
            interest_vector=interest_vector,
            top_k=1000,
            topic_keywords=topic_keywords,
        )
        all_dicts = [article_to_dict(a) for a in ranked]
        _set_recs_cache(current_user.id, all_dicts)
        total = len(all_dicts)
        offset = (page - 1) * per_page
        return {
            "articles": all_dicts[offset:offset + per_page],
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page or 1,
        }

    # Build user embedding: mean(liked) − 0.3 × mean(disliked), then normalize
    user_emb = np.mean(liked_embeddings, axis=0)
    if disliked_embeddings:
        user_emb = user_emb - 0.3 * np.mean(disliked_embeddings, axis=0)
    norm = np.linalg.norm(user_emb)
    if norm > 0:
        user_emb = user_emb / norm

    all_articles = db.query(News).filter(News.embedding != None, News.summary.isnot(None)).all()
    ranked = ranker.rank_articles(all_articles, user_emb.tolist(), interest_vector, top_k=1000, topic_keywords=topic_keywords)

    all_dicts = [article_to_dict(a) for a in ranked]
    _set_recs_cache(current_user.id, all_dicts)
    total = len(all_dicts)
    offset = (page - 1) * per_page
    return {
        "articles": all_dicts[offset:offset + per_page],
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": (total + per_page - 1) // per_page or 1,
    }
