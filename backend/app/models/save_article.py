from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base import Base


class SavedArticle(Base):
    __tablename__ = "saved_articles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    article_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("news.article_id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    saved_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    user = relationship("User", backref="saved_articles")
    article = relationship("News", backref="saved_by_users")