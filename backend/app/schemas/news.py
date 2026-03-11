"""Pydantic schemas for Article — response shapes and feed pagination."""

# TODO: Import BaseModel from pydantic
# TODO: Import Optional, List, datetime


class ArticleOut:
    """Single article as returned by the feed / recommendations endpoints."""
    # TODO: id, title, description, url, source, category,
    #       published_at, summary, created_at
    # TODO: model_config = {"from_attributes": True}
    pass


class ArticleFeedResponse:
    """Paginated feed response."""
    # TODO: articles: List[ArticleOut]
    # TODO: total: int
    # TODO: page: int
    # TODO: per_page: int
    pass
