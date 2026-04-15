from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ARRAY
from ..db.base import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    preview = Column(Text, nullable=True)
    cover_image = Column(Text, nullable=True)
    published_at = Column(DateTime, nullable=True)
    content = Column(Text, nullable=True)
    source = Column(String(255), nullable=True)
    keywords = Column(ARRAY(String), nullable=True)
    category = Column(String(100), nullable=True)
    author = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())