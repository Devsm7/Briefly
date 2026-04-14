from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ARRAY
from app.db.base import Base


class UserInterestProfile(Base):
    __tablename__ = "user_interest_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_identifier = Column(String(100), nullable=False, unique=True)
    saved_articles = Column(ARRAY(String), nullable=True)
    interests_based_on_interaction = Column(ARRAY(String), nullable=True)
    keywords = Column(ARRAY(String), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())