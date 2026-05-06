"""
News and saved-article data access — all DB reads/writes for articles go through here.

Models used:
  News          — article records (title, content, summary, embedding, etc.)
  SavedArticle  — user bookmarks (user_id → article_id)

───────────────────────────────────────────────────────────────────────────────
NOTE ON EMBEDDINGS (not yet implemented):
  Article embeddings (384-dim vectors via sentence-transformers) are stored in
  News.embedding.  When recommender/embedder.py is live, a background job
  populates this column.  The recommender/ranker.py (Ranker class) then uses
  cosine similarity between News.embedding and the user's interest_vector to
  rank articles.  No code here needs to change when that pipeline goes live —
  the ranker reads News.embedding and survey_preferences.interest_vector.
───────────────────────────────────────────────────────────────────────────────
"""

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.news import News
from app.models.save_article import SavedArticle


def _article_to_dict(article: News) -> dict:
    """Map a News ORM object to a dict matching the expected frontend schema."""
    return {
        "article_id": article.article_id,
        "title": article.title,
        "preview": article.summary if article.summary else article.description,
        "cover_image": article.image_url,
        "date": article.published_date,
        "content": article.content,
        "source": article.source,
        "url": article.url,
        "category": article.category,
        "author": article.author,
    }


class NewsService:
    """All DB operations for news articles and saved bookmarks."""

    def get_news(self) -> list[dict]:
        """
        Return all articles that have a summary (fully processed).
        An article without a summary is skipped — it hasn't been enriched yet.
        """
        db = SessionLocal()
        try:
            articles = db.query(News).filter(News.summary.isnot(None)).all()
            return [_article_to_dict(a) for a in articles]
        finally:
            db.close()

    def save_article_for_user(self, user_id: int, article_id: int) -> SavedArticle:
        """Bookmark an article for a user. Idempotent — returns existing record."""
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
            saved = SavedArticle(user_id=user_id, article_id=article_id)
            db.add(saved)
            db.commit()
            db.refresh(saved)
            return saved
        finally:
            db.close()

    def get_saved_articles(self, user_id: int) -> list[dict]:
        """Return all saved articles for a user, newest first, only if they have a summary."""
        db = SessionLocal()
        try:
            rows = (
                db.query(SavedArticle)
                .join(News, SavedArticle.article_id == News.article_id)
                .filter(SavedArticle.user_id == user_id)
                .filter(News.summary.isnot(None))
                .order_by(SavedArticle.saved_at.desc())
                .all()
            )
            return [_article_to_dict(row.article) for row in rows]
        finally:
            db.close()

    def remove_saved_article(self, user_id: int, article_id: int) -> bool:
        """Remove a bookmark. Returns True if deleted, False if it didn't exist."""
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

    def is_article_saved(self, user_id: int, article_id: int) -> bool:
        """Check whether an article is bookmarked by the user."""
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


def search_articles(
        self,
        query: str | None = None,
        category: str | None = None,
        limit: int = 10,
    ) -> list[dict]:
        """
        Semantic search using article embeddings + keyword fallback.

        1. If query is provided, embed it and find similar articles by cosine similarity.
        2. If no articles have embeddings, fall back to keyword ilike on title/description.
        3. Filter by category if provided.
        4. Return up to `limit` results ordered by relevance score.
        """
        from app.recommender.embedder import Embedder
        from app.recommender.ranker import Ranker

        db = SessionLocal()
        try:
            q = db.query(News).filter(News.summary.isnot(None))

            if category:
                q = q.filter(News.category == category.lower())

            articles = q.all()

            # Semantic search via embeddings
            if query:
                embedder = Embedder()
                ranker = Ranker()
                query_embedding = embedder.embed_text(query)

                scored = []
                for article in articles:
                    if article.embedding:
                        score = ranker.cosine_similarity(query_embedding, article.embedding)
                        scored.append((score, article))
                    elif article.title:
                        # Keyword fallback: title match
                        if query.lower() in article.title.lower():
                            scored.append((0.0, article))

                scored.sort(key=lambda x: x[0], reverse=True)
                articles = [a for _, a in scored[:limit]]
            else:
                articles = articles[:limit]

            return [_article_to_dict(a) for a in articles]
        finally:
            db.close()