"""UserInteraction ORM model — maps to the `user_interactions` table."""

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class UserInteraction(Base):
    __tablename__ = "user_interactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    article_id: Mapped[int] = mapped_column(Integer, ForeignKey("news.article_id", ondelete="CASCADE"), index=True, nullable=False)
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    read_time: Mapped[float | None] = mapped_column(Float, nullable=True)
    scroll_depth: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", backref="interactions")
    article = relationship("News", backref="interactions")
