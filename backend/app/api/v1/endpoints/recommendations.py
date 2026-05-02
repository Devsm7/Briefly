"""Personalized recommendation endpoints."""

import logging

import numpy as np
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.news import News
from app.models.survey import SurveyPreference
from app.models.user import User
from app.models.user_interaction import UserInteraction
from app.recommender.ranker import Ranker

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/recommendations", tags=["recommendations"])
ranker = Ranker()


@router.get("")
def get_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """GET /recommendations — Return top-20 personalized articles for the current user."""
    survey = db.query(SurveyPreference).filter(
        SurveyPreference.user_id == current_user.id
    ).first()
    interest_vector = survey.interest_vector if survey else {}

    # Collect liked and disliked article IDs
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

    # Fallback — no likes yet: return recent articles from top survey categories
    if not liked_embeddings:
        top_categories = sorted(interest_vector, key=interest_vector.get, reverse=True)[:2]
        query = db.query(News).order_by(News.created_at.desc())
        if top_categories:
            query = query.filter(News.category.in_(top_categories))
        return query.limit(20).all()

    # Build user embedding: mean(liked) − 0.3 × mean(disliked), then normalize
    user_emb = np.mean(liked_embeddings, axis=0)
    if disliked_embeddings:
        user_emb = user_emb - 0.3 * np.mean(disliked_embeddings, axis=0)
    norm = np.linalg.norm(user_emb)
    if norm > 0:
        user_emb = user_emb / norm

    articles = db.query(News).filter(News.embedding != None).all()
    return ranker.rank_articles(articles, user_emb.tolist(), interest_vector, top_k=20)
