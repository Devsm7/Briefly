"""News feed endpoints."""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.api.deps import get_current_user
from app.core.security import decode_token
from app.models.user import User
from app.services.news_service import news_service
from app.tasks.scheduler import run_embed_job, run_scrape_job

_optional_bearer = HTTPBearer(auto_error=False)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/news", tags=["news"])


@router.post("/fetch", status_code=status.HTTP_200_OK)
def trigger_fetch():
    """POST /news/fetch — Manually trigger a full news scrape and insert into DB."""
    try:
        run_scrape_job()
        return {"status": "done"}
    except Exception as exc:
        logger.error("Manual fetch failed: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fetch failed: {exc}",
        ) from exc


@router.post("/embed", status_code=status.HTTP_200_OK)
def trigger_embed():
    """POST /news/embed — Manually trigger embedding for un-embedded articles."""
    try:
        run_embed_job()
        return {"status": "done"}
    except Exception as exc:
        logger.error("Manual embed failed: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Embed failed: {exc}",
        ) from exc


@router.get("")
def list_articles(page: int = 1, per_page: int = 50):
    """
    GET /news — Return paginated articles.

    Query params:
      page     — page number, 1-indexed (default 1)
      per_page — articles per page (default 50, max 100)
    """
    if page < 1:
        raise HTTPException(status_code=400, detail="page must be >= 1")
    if per_page < 1 or per_page > 100:
        raise HTTPException(status_code=400, detail="per_page must be between 1 and 100")
    try:
        articles, total = news_service.get_news(page=page, per_page=per_page)
        return {
            "articles": articles,
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page,
        }
    except Exception as exc:
        logger.error("Failed to load news feed: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not load articles: {exc}",
        ) from exc


@router.get("/search")
def search_articles(
    q: str | None = None,
    category: str | None = None,
    limit: int = 10,
):
    """
    GET /news/search?q=<query>&category=<cat>&limit=<n>
    Semantic search using article embeddings.
    Falls back to keyword match on title if embeddings are missing.
    Requires q (search query) — returns 400 if empty.
    """
    if q is not None and q.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="q cannot be empty",
        )
    try:
        return news_service.search_articles(query=q, category=category, limit=limit)
    except Exception as exc:
        logger.error("Search failed: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {exc}",
        ) from exc


@router.get("/overall")
def get_overall_summary(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(_optional_bearer),
):
    """
    GET /news/overall
    Returns a personalized AI news brief ordered by the user's survey interest scores.
    Auth is optional — unauthenticated callers get a generic global brief.
    """
    user_id: Optional[int] = None
    if credentials:
        payload = decode_token(credentials.credentials)
        if payload and payload.get("sub"):
            try:
                user_id = int(payload["sub"])
            except (ValueError, TypeError):
                pass
    try:
        return {"summary": news_service.get_overall_summary(user_id=user_id)}
    except Exception as exc:
        logger.error("Overall summary failed: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Overall summary generation failed.",
        ) from exc


@router.get("/digest")
def get_category_digests():
    """
    GET /news/digest
    Returns an AI-generated overall summary for each category.
    Each digest synthesizes all summarized articles in that category.
    """
    try:
        return news_service.get_category_digests()
    except Exception as exc:
        logger.error("Digest generation failed: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Digest failed: {exc}",
        ) from exc


@router.get("/library")
def get_library(current_user: User = Depends(get_current_user)):
    """GET /news/library — Saved articles for the current user."""
    return news_service.get_saved_articles(current_user.id)


@router.get("/{article_id}")
def get_article(article_id: int):
    """GET /news/{article_id} — Return a single article by ID."""
    article = news_service.get_article_by_id(article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@router.get("/saved/{article_id}")
def check_saved(
    article_id: int,
    current_user: User = Depends(get_current_user),
):
    """GET /news/saved/{article_id} — Check whether an article is bookmarked."""
    return {"saved": news_service.is_article_saved(current_user.id, article_id)}


@router.post("/save/{article_id}", status_code=status.HTTP_201_CREATED)
def save_article(
    article_id: int,
    current_user: User = Depends(get_current_user),
):
    """POST /news/save/{article_id} — Bookmark an article."""
    news_service.save_article_for_user(current_user.id, article_id)
    return {"saved": True}


@router.delete("/save/{article_id}")
def unsave_article(
    article_id: int,
    current_user: User = Depends(get_current_user),
):
    """DELETE /news/save/{article_id} — Remove a bookmark."""
    removed = news_service.remove_saved_article(current_user.id, article_id)
    if not removed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not in library")
    return {"saved": False}
