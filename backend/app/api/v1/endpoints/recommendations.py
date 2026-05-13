"""Personalized recommendation endpoints."""

import logging

import numpy as np
from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_current_user, get_db
from app.models.news import News
from app.models.survey import SurveyPreference
from app.models.user import User
from app.models.user_interaction import UserInteraction
from app.recommender.ranker import Ranker
from app.services.news_service import article_to_dict, build_user_embedding_from_categories
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/recommendations", tags=["recommendations"])
ranker = Ranker()


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

    # Fallback — no likes yet: rank all articles by survey interest_vector
    if not liked_embeddings:
        all_articles = db.query(News).filter(News.summary.isnot(None)).all()

        if survey and survey.user_embedding is not None:
            user_emb = survey.user_embedding  # cache hit
        else:
            # Build from existing article embeddings in DB — no Groq call needed
            user_emb = build_user_embedding_from_categories(db, interest_vector)
            if survey and user_emb:
                survey.user_embedding = user_emb
                db.commit()

        ranked = ranker.rank_articles(
            all_articles,
            user_embedding=user_emb,
            interest_vector=interest_vector,
            top_k=1000,
        )
        total = len(ranked)
        offset = (page - 1) * per_page
        page_articles = ranked[offset:offset + per_page]
        return {
            "articles": [article_to_dict(a) for a in page_articles],
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page or 1,
        }

    # Build user embedding: blend AI-generated interest base with user feedback signal
    # base = interest description embedding (if available)
    # feedback = mean(liked) − 0.3 × mean(disliked)
    # final = 0.4 × base + 0.6 × feedback (feedback dominates as it is more personal)
    interest_description = generate_user_interest_description(interest_vector)
    base_emb = embedder.embed_text(interest_description) if interest_description else None

    feedback_emb = np.mean(liked_embeddings, axis=0)
    if disliked_embeddings:
        feedback_emb = feedback_emb - 0.3 * np.mean(disliked_embeddings, axis=0)

    if base_emb is not None:
        base_arr = np.array(base_emb)
        norm = np.linalg.norm(base_arr)
        if norm > 0:
            base_arr = base_arr / norm
        user_emb = 0.4 * base_arr + 0.6 * feedback_emb
    else:
        user_emb = feedback_emb

    norm = np.linalg.norm(user_emb)
    if norm > 0:
        user_emb = user_emb / norm
    else:
        user_emb = None

    all_articles = db.query(News).filter(News.embedding != None, News.summary.isnot(None)).all()
    ranked = ranker.rank_articles(all_articles, user_emb.tolist(), interest_vector, top_k=1000)

    total = len(ranked)
    offset = (page - 1) * per_page
    page_articles = ranked[offset:offset + per_page]
    return {
        "articles": [article_to_dict(a) for a in page_articles],
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": (total + per_page - 1) // per_page or 1,
    }
