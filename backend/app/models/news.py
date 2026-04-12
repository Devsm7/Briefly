from sqlalchemy import Column, Integer, String, Text

from app.db.base import Base


class News(Base):
    __tablename__ = "news"

    article_id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text)
    url = Column(String, unique=True)
    category = Column(String)
    source = Column(String)
    published_date = Column(String)
    image_url = Column(String, nullable=True)
    language = Column(String, nullable=True)
