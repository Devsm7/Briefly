from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.article import Base, Article
from app.models.user_interest_profile import UserInterestProfile


DATABASE_URL = "postgresql://neondb_owner:npg_LINU7mylfe8w@ep-wandering-frost-an5bxlnm-pooler.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=requir"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    Base.metadata.create_all(bind=engine)


def insert_article(title, preview=None, cover_image=None, published_at=None,
                   content=None, source=None, keywords=None,
                   category=None, author=None):
    db = SessionLocal()
    article = Article(
        title=title,
        preview=preview,
        cover_image=cover_image,
        published_at=published_at,
        content=content,
        source=source,
        keywords=keywords or [],
        category=category,
        author=author
    )
    db.add(article)
    db.commit()
    db.refresh(article)
    db.close()
    return article


def get_articles():
    db = SessionLocal()
    articles = db.query(Article).all()
    db.close()
    return articles


def get_article_by_id(article_id):
    db = SessionLocal()
    article = db.query(Article).filter(Article.id == article_id).first()
    db.close()
    return article


def insert_user_interest_profile(user_identifier, saved_articles=None,
                                 interests_based_on_interaction=None, keywords=None):
    db = SessionLocal()
    profile = UserInterestProfile(
        user_identifier=user_identifier,
        saved_articles=saved_articles or [],
        interests_based_on_interaction=interests_based_on_interaction or [],
        keywords=keywords or []
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    db.close()
    return profile


def get_user_interest_profile(user_identifier):
    db = SessionLocal()
    profile = db.query(UserInterestProfile).filter(
        UserInterestProfile.user_identifier == user_identifier
    ).first()
    db.close()
    return profile


def update_user_interest_profile(user_identifier, saved_articles=None,
                                 interests_based_on_interaction=None, keywords=None):
    db = SessionLocal()
    profile = db.query(UserInterestProfile).filter(
        UserInterestProfile.user_identifier == user_identifier
    ).first()

    if not profile:
        db.close()
        return None

    if saved_articles is not None:
        profile.saved_articles = saved_articles

    if interests_based_on_interaction is not None:
        profile.interests_based_on_interaction = interests_based_on_interaction

    if keywords is not None:
        profile.keywords = keywords

    db.commit()
    db.refresh(profile)
    db.close()
    return profile


if __name__ == "__main__":
    create_tables()