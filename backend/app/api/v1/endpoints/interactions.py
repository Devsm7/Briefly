"""User interaction tracking — likes and dislikes update the user interest profile."""

import logging

import numpy as np
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.news import News
from app.models.survey import SurveyPreference
from app.models.user import User
from app.models.user_interaction import UserInteraction
from app.recommender.interest_vector import interest_vector_svc
from app.schemas.interaction import InteractionCreate, InteractionOut

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/interactions", tags=["interactions"])


@router.post("", response_model=InteractionOut, status_code=201)
def log_interaction(
    payload: InteractionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    POST /interactions
    Record a like or dislike. For like/dislike actions:
      - Adjusts the user's category interest_vector (±0.05)
      - Incrementally updates the user's cached embedding toward/away from the article
    """
    interaction = UserInteraction(
        user_id=current_user.id,
        article_id=payload.article_id,
        action=payload.action,
        read_time=payload.read_time,
        scroll_depth=payload.scroll_depth,
    )
    db.add(interaction)

    if payload.action in ("like", "dislike"):
        article = db.query(News).filter(News.article_id == payload.article_id).first()
        survey = db.query(SurveyPreference).filter(
            SurveyPreference.user_id == current_user.id
        ).first()

        if article and survey:
            # Update category interest weights
            new_vector = interest_vector_svc.update_from_feedback(
                survey.interest_vector or {}, article.category, payload.action
            )
            survey.interest_vector = new_vector

            # Incrementally move user embedding toward (like) or away (dislike) from article
            if article.embedding:
                article_emb = np.array(article.embedding, dtype=float)
                current_emb = survey.user_embedding
                emb = np.array(current_emb, dtype=float) if current_emb else np.zeros_like(article_emb)

                if payload.action == "like":
                    emb = emb + article_emb
                else:
                    emb = emb - 0.3 * article_emb

                norm = np.linalg.norm(emb)
                survey.user_embedding = (emb / norm).tolist() if norm > 0 else emb.tolist()

    db.commit()
    db.refresh(interaction)
    logger.debug("Recorded %s interaction: user=%d article=%d", payload.action, current_user.id, payload.article_id)
    return interaction
