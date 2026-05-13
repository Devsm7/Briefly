"""SurveyPreference ORM model — maps to the `survey_preferences` table."""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, SmallInteger, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base import Base


class SurveyPreference(Base):
    __tablename__ = "survey_preferences"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    # Selected categories e.g. ["tech", "politics", "sport"]
    categories: Mapped[list] = mapped_column(JSONB, default=list, nullable=False, server_default="[]")

    # All question answers e.g. {"Q01": "daily", "Q05": 4, "Q02": ["articles"]}
    answers: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False, server_default="{}")

    # Derived weights for recommendation engine e.g. {"tech": 0.8, "politics": 0.6}
    interest_vector: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False, server_default="{}")

    # Cached 384-dim user embedding. Null until first recommendations request; invalidated on survey change.
    user_embedding: Mapped[list | None] = mapped_column(JSONB, nullable=True, default=None)

    # 0 = skipped / partial, 1 = completed
    survey_completed: Mapped[int] = mapped_column(SmallInteger, default=0, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    #user = relationship("User", back_populates="survey")
