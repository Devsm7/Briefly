from sqlalchemy import Column, DateTime, Float, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql import func

from ..db.base import Base


class News(Base):
    __tablename__ = "news"

    article_id = Column(Integer, primary_key=True, index=True)

    # NewsData.io deduplication key (their `article_id` field, e.g. "en123456")
    newsdata_id = Column(String(100), unique=True, nullable=True, index=True)

    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)       # NewsData `description`
    content = Column(Text, nullable=True)            # NewsData `content` (may be truncated)
    url = Column(String, unique=True, nullable=True, index=True)
    image_url = Column(String, nullable=True)
    published_date = Column(String, nullable=True)   # stored as string from API (ISO-ish)
    source = Column(String, nullable=True)           # NewsData `source_id`
    category = Column(String(100), nullable=True)
    language = Column(String(10), nullable=True, default="en")
    keywords = Column(ARRAY(String), nullable=True)
    author = Column(String(255), nullable=True)      # NewsData `creator` (list → joined)

    # 384-dim sentence-transformer vector (populated by embedding job)
    embedding = Column(ARRAY(Float), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
