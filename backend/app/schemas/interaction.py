"""Pydantic schemas for user interaction events."""

from datetime import datetime
from pydantic import BaseModel


class InteractionCreate(BaseModel):
    article_id: int
    action: str  # "like" | "dislike"
    read_time: float | None = None
    scroll_depth: float | None = None


class InteractionOut(BaseModel):
    id: int
    user_id: int
    article_id: int
    action: str
    created_at: datetime
    model_config = {"from_attributes": True}
