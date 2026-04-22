"""News feed endpoints."""

import logging

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_user
from app.models.user import User
from app.services.db_all_articles import (
    get_news,
    get_saved_articles,
    is_article_saved,
    remove_saved_article,
    save_article_for_user,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/news", tags=["news"])


@router.get("")
def list_articles():
    """GET /news — Return all articles."""
    try:
        return get_news()
    except Exception as exc:
        logger.error("Failed to load news feed: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not load articles: {exc}",
        ) from exc


@router.get("/library")
def get_library(current_user: User = Depends(get_current_user)):
    """GET /news/library — Saved articles for the current user."""
    return get_saved_articles(current_user.id)


@router.get("/saved/{article_id}")
def check_saved(
    article_id: int,
    current_user: User = Depends(get_current_user),
):
    """GET /news/saved/{article_id} — Check whether an article is bookmarked."""
    return {"saved": is_article_saved(current_user.id, article_id)}


@router.post("/save/{article_id}", status_code=status.HTTP_201_CREATED)
def save_article(
    article_id: int,
    current_user: User = Depends(get_current_user),
):
    """POST /news/save/{article_id} — Bookmark an article."""
    save_article_for_user(current_user.id, article_id)
    return {"saved": True}


@router.delete("/save/{article_id}")
def unsave_article(
    article_id: int,
    current_user: User = Depends(get_current_user),
):
    """DELETE /news/save/{article_id} — Remove a bookmark."""
    removed = remove_saved_article(current_user.id, article_id)
    if not removed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not in library")
    return {"saved": False}
