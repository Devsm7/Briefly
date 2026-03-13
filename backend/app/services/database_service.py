from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from modell.user import Base, User
from modell.survey_preference import SurveyPreference
from modell.news import News
from modell.user_interaction import UserInteraction
from modell.saved_article import SavedArticle


DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/briefly_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    Base.metadata.create_all(bind=engine)


def insert_user(email, password):
    db = SessionLocal()
    user = User(email=email, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user


def insert_survey_preference(user_id, category):
    db = SessionLocal()
    preference = SurveyPreference(user_id=user_id, category=category)
    db.add(preference)
    db.commit()
    db.refresh(preference)
    db.close()
    return preference


def insert_article(title, description, url, category, source, published_date):
    db = SessionLocal()
    article = News(
        title=title,
        description=description,
        url=url,
        category=category,
        source=source,
        published_date=published_date
    )
    db.add(article)
    db.commit()
    db.refresh(article)
    db.close()
    return article


def get_news():
    db = SessionLocal()
    articles = db.query(News).all()
    db.close()
    return articles


def log_interaction(user_id, article_id, interaction_type):
    db = SessionLocal()
    interaction = UserInteraction(
        user_id=user_id,
        article_id=article_id,
        interaction_type=interaction_type
    )
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    db.close()
    return interaction


if __name__ == "__main__":
    create_tables()