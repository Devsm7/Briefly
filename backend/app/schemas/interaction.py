"""Pydantic schemas for user interaction events."""

# TODO: Import BaseModel from pydantic
# TODO: Import Optional, datetime


class InteractionCreate:
    """Payload for POST /interactions."""
    # TODO: article_id: int
    # TODO: action: str  —  "view" | "like" | "dislike" | "save"
    #                        | "unsave" | "more_like_this" | "less_like_this"
    # TODO: read_time: Optional[float] = None    (seconds)
    # TODO: scroll_depth: Optional[float] = None (0.0 – 1.0)
    pass


class InteractionOut:
    """Interaction record as returned by the API."""
    # TODO: id, user_id, article_id, action, read_time, scroll_depth, created_at
    # TODO: model_config = {"from_attributes": True}
    pass
