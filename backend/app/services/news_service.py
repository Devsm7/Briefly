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

from collections import defaultdict

import numpy as np
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.news import News
from app.models.save_article import SavedArticle
from app.services.summarizer import generate_category_summary


def build_user_embedding_from_categories(
    db: Session,
    interest_vector: dict[str, float],
    answers: dict | None = None,
    articles_per_cat: int = 20,
) -> list[float] | None:
    """
    Build a cold-start user embedding from existing article embeddings in the DB.

    When the user has selected subtopics (e.g. tech → cybersecurity), articles in that
    category are scored by cosine similarity to the topic labels and the most relevant
    ones are used — so cybersecurity articles dominate over generic tech noise.
    Falls back to most-recent articles when no subtopics are selected.
    """
    from app.recommender.embedder import embedder
    from app.recommender.ranker import Ranker
    from app.services.summarizer import _TOPIC_LABELS, _TOPIC_QUESTION

    ranker = Ranker()

    if not interest_vector:
        return None

    weighted_sum = None
    total_weight = 0.0

    for cat, weight in interest_vector.items():
        if weight <= 0.1:
            continue

        # Fetch a larger pool — we'll re-rank by topic similarity below
        articles = (
            db.query(News)
            .filter(News.category == cat, News.embedding.isnot(None))
            .order_by(News.created_at.desc())
            .limit(200)
            .all()
        )
        if not articles:
            continue

        # If user picked subtopics, find articles closest to those topics
        topic_codes = (answers or {}).get(_TOPIC_QUESTION.get(cat, ""), [])
        if topic_codes and isinstance(topic_codes, list):
            labels = [_TOPIC_LABELS.get(cat, {}).get(code, code) for code in topic_codes]
            topic_emb = embedder.embed_text(" ".join(labels))
            articles = sorted(
                articles,
                key=lambda a: ranker.cosine_similarity(topic_emb, a.embedding),
                reverse=True,
            )

        selected = articles[:articles_per_cat]
        cat_embs = np.array([a.embedding for a in selected], dtype=float)
        cat_mean = cat_embs.mean(axis=0)

        weighted_sum = (weight * cat_mean) if weighted_sum is None else (weighted_sum + weight * cat_mean)
        total_weight += weight

    if weighted_sum is None or total_weight == 0:
        return None

    norm = np.linalg.norm(weighted_sum)
    return (weighted_sum / norm).tolist() if norm > 0 else weighted_sum.tolist()


def article_to_dict(article: News) -> dict:
    """Map a News ORM object to a dict matching the expected frontend schema."""
    if article.language == "ar" and article.summary_ar:
        preview = article.summary_ar
    elif article.summary:
        preview = article.summary
    else:
        preview = article.description

    return {
        "article_id": article.article_id,
        "title": article.title,
        "preview": preview,
        "cover_image": article.image_url,
        "date": article.published_date,
        "content": article.content,
        "source": article.source,
        "url": article.url,
        "category": article.category,
        "author": article.author,
        "language": article.language,
    }


class NewsService:
    """All DB operations for news articles and saved bookmarks."""

    def get_news(self, page: int = 1, per_page: int = 50) -> tuple[list[dict], int]:
        """
        Return paginated articles that have a summary (fully processed).

        Returns (articles, total_count) so the frontend can render page controls.
        """
        db = SessionLocal()
        try:
            total = db.query(News).filter(News.summary.isnot(None)).count()
            offset = (page - 1) * per_page
            articles = (
                db.query(News)
                .filter(News.summary.isnot(None))
                .order_by(News.created_at.desc())
                .offset(offset)
                .limit(per_page)
                .all()
            )
            return [article_to_dict(a) for a in articles], total
        finally:
            db.close()

    def get_article_by_id(self, article_id: int) -> dict | None:
        """Return a single article by ID, or None if not found."""
        db = SessionLocal()
        try:
            article = db.query(News).filter(News.article_id == article_id).first()
            return article_to_dict(article) if article else None
        finally:
            db.close()

    def get_articles_by_category(self, category: str) -> list[dict]:
        """Return all articles with summaries for a given category."""
        db = SessionLocal()
        try:
            articles = (
                db.query(News)
                .filter(News.category == category.lower())
                .filter(News.summary.isnot(None))
                .all()
            )
            return [article_to_dict(a) for a in articles]
        finally:
            db.close()

    def get_overall_summary(self, user_id: int | None = None) -> str:
        """Generate a news brief, personalized by user interest scores if user_id is provided."""
        from app.models.survey import SurveyPreference
        from app.services.summarizer import generate_overall_summary
        db = SessionLocal()
        try:
            interest_vector = None
            if user_id:
                pref = db.query(SurveyPreference).filter(
                    SurveyPreference.user_id == user_id,
                    SurveyPreference.survey_completed == 1,
                ).first()
                if pref and pref.interest_vector:
                    interest_vector = pref.interest_vector
            summary = generate_overall_summary(db, interest_vector=interest_vector)
            return summary or "No articles available to summarize."
        finally:
            db.close()

    def get_category_digests(self) -> dict[str, str]:
        """
        Generate an AI digest for each category that has summarized articles.
        Returns { category: digest_text } for categories with articles.
        """
        db = SessionLocal()
        try:
            articles = db.query(News).filter(News.summary.isnot(None)).all()
            by_category: dict[str, list[dict]] = defaultdict(list)
            for a in articles:
                if a.category:
                    by_category[a.category.lower()].append(article_to_dict(a))

            digests = {}
            for category, arts in by_category.items():
                digest = generate_category_summary(arts, category)
                if digest:
                    digests[category] = digest

            return digests
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
            return [article_to_dict(row.article) for row in rows]
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
        Semantic + keyword hybrid search.

        1. Embed query → cosine similarity against article embedding (summary).
        2. Keyword boost: title match → small additive bonus.
        3. Filter by category if provided.
        4. Return top `limit` results sorted by final score.
        """
        from app.recommender.embedder import Embedder
        from app.recommender.ranker import Ranker

        db = SessionLocal()
        try:
            q = db.query(News).filter(News.summary.isnot(None))

            if category:
                q = q.filter(News.category == category.lower())

            articles = q.all()

            if not query:
                return [article_to_dict(a) for a in articles[:limit]]

            embedder = Embedder()
            ranker = Ranker()
            query_embedding = embedder.embed_text(query)
            query_lower = query.lower()

            scored = []
            for article in articles:
                base_score = 0.0

                if article.embedding:
                    base_score = ranker.cosine_similarity(query_embedding, article.embedding)

                # Keyword boost: title or description match
                title_match = article.title and query_lower in article.title.lower()
                desc_match = article.description and query_lower in article.description.lower()

                keyword_bonus = 0.0
                if title_match:
                    keyword_bonus = 0.15
                if desc_match and not title_match:
                    keyword_bonus = 0.05

                final_score = base_score + keyword_bonus
                scored.append((final_score, article))

            scored.sort(key=lambda x: x[0], reverse=True)
            return [article_to_dict(a) for _, a in scored[:limit]]
        finally:
            db.close()


news_service = NewsService()