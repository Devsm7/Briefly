from ..db.base import Base
from ..db.session import SessionLocal, engine
from ..models.article import Article as News
from ..models.saved_article import SavedArticle
from ..models.survey import SurveyPreference
from ..models.user import User
from ..models.user_interaction import UserInteraction


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


def insert_article(title, description, url, category, source, published_date, imgURL, language):
    db = SessionLocal()
    article = News(
        title=title,
        image_url=imgURL,
        description=description,
        url=url,
        category=category,
        source=source,
        published_date=published_date,
        language=language,
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
        action=interaction_type,
    )
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    db.close()
    return interaction


if __name__ == "__main__":
    create_tables()
