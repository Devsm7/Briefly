from ..db.session import SessionLocal
from ..models.news import News
from ..models.save_article import SavedArticle


def get_news():
    db = SessionLocal()
    try:
        articles = db.query(News).all()

        return [
            {
                "article_id": article.article_id,
                "title": article.title,
                "preview": article.description,
                "cover_image": article.image_url,
                "date": article.published_date,
                "content": article.content,
                "source": article.source,
                "url": article.url,
                "category": article.category,
                "author": article.author,
            }
            for article in articles
        ]
    finally:
        db.close()


def save_article_for_user(user_id: int, article_id: int):
    db = SessionLocal()
    try:
        existing = (
            db.query(SavedArticle)
            .filter(
                SavedArticle.user_id == user_id,
                SavedArticle.article_id == article_id,
            )
            .first()
        )

        if existing:
            return existing

        saved_article = SavedArticle(
            user_id=user_id,
            article_id=article_id,
        )

        db.add(saved_article)
        db.commit()
        db.refresh(saved_article)
        return saved_article

    finally:
        db.close()


def get_saved_articles(user_id: int):
    db = SessionLocal()
    try:
        saved_rows = (
            db.query(SavedArticle)
            .join(News, SavedArticle.article_id == News.article_id)
            .filter(SavedArticle.user_id == user_id)
            .order_by(SavedArticle.saved_at.desc())
            .all()
        )

        return [
            {
                "article_id": row.article.article_id,
                "title": row.article.title,
                "preview": row.article.description,
                "cover_image": row.article.image_url,
                "date": row.article.published_date,
                "content": row.article.content,
                "source": row.article.source,
                "url": row.article.url,
                "category": row.article.category,
                "author": row.article.author,
            }
            for row in saved_rows
        ]
    finally:
        db.close()

def remove_saved_article(user_id: int, article_id: int):
    db = SessionLocal()
    try:
        saved = (
            db.query(SavedArticle)
            .filter(
                SavedArticle.user_id == user_id,
                SavedArticle.article_id == article_id,
            )
            .first()
        )

        if not saved:
            return False 

        db.delete(saved)
        db.commit()
        return True

    finally:
        db.close()
 
def is_article_saved(user_id: int, article_id: int):
    db = SessionLocal()
    try:
        return (
            db.query(SavedArticle)
            .filter(
                SavedArticle.user_id == user_id,
                SavedArticle.article_id == article_id,
            )
            .first()
            is not None
        )
    finally:
        db.close()
