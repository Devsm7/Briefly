"""NewsData.io API client — fetches articles and upserts them into the news table."""

import logging

import requests
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.news import News
from app.services.content_enricher import resolve_content
from app.services.summarizer import generate_summary
from app.recommender.embedder import embedder


logger = logging.getLogger(__name__)

# Map NewsData category slugs → internal categories
_CATEGORY_MAP: dict[str, str] = {
    "technology": "tech",
    "science": "tech",
    "sports": "sport",
    "politics": "politics",
    "business": "business",
    "entertainment": "entertainment",
    "health": "health",
    "world": "world",
    "environment": "environment",
    "food": "food",
    "tourism": "tourism",
    "top": "top",
}

# Fetch parameters
_DEFAULT_CATEGORIES = ["business", "sports", "politics", "technology", "science"]
_DEFAULT_COUNTRIES  = "sa,cn,us"
_DEFAULT_LANGUAGES  = "ar,en"


def _map_article(raw: dict) -> dict:
    """Map a raw NewsData result dict to News model kwargs."""
    # creator is a list or None
    creators = raw.get("creator") or []
    author = ", ".join(creators) if creators else None

    # category is a list in NewsData — take first and map to internal
    categories = raw.get("category") or []
    raw_cat = categories[0] if categories else None
    category = _CATEGORY_MAP.get(raw_cat, raw_cat)  # pass through if unmapped

    return {
        "newsdata_id": raw.get("article_id"),
        "title": (raw.get("title") or "").strip(),
        "description": (raw.get("description") or "").strip() or None,
        "content": resolve_content(raw),
        "url": raw.get("link"),
        "image_url": raw.get("image_url"),
        "published_date": raw.get("pubDate"),
        "source": raw.get("source_id"),
        "category": category,
        "language": (raw.get("language") or "en").lower(),
        "keywords": raw.get("keywords") or [],
        "author": author,
    }


class NewsdataService:
    """Fetches from NewsData.io and upserts articles into the database."""

    def __init__(self) -> None:
        self._base_url = settings.NEWSDATA_BASE_URL
        self._api_key = settings.NEWSDATA_API_KEY

    def fetch_by_category(
        self,
        category: str,
        language: str = _DEFAULT_LANGUAGES,
        country: str = _DEFAULT_COUNTRIES,
        max_pages: int = 3,
    ) -> list[dict]:
        """
        Fetch up to `max_pages` pages of articles for one NewsData category.
        Returns a flat list of raw article dicts.
        """
        results: list[dict] = []
        next_page: str | None = None

        for page_num in range(max_pages):
            params: dict = {
                "apikey": self._api_key,
                "category": category,
                "language": language,
                "country": country,
                "image": 1,          # only articles with images
                "video": 0,          # exclude video articles
                "removeduplicate": 1,
            }
            if next_page:
                params["page"] = next_page

            try:
                response = requests.get(
                    f"{self._base_url}/latest",
                    params=params,
                    timeout=15,
                )
                response.raise_for_status()
                data = response.json()
            except requests.RequestException as exc:
                logger.error("NewsData fetch failed [category=%s page=%d]: %s", category, page_num, exc)
                break

            if data.get("status") != "success":
                logger.error("NewsData error response [category=%s]: %s", category, data)
                break

            page_results = data.get("results") or []
            results.extend(page_results)
            logger.info("Fetched %d articles [category=%s page=%d]", len(page_results), category, page_num)

            next_page = data.get("nextPage")
            if not next_page:
                break  # no more pages

        return results

    def fetch_all_categories(
        self,
        categories: list[str] | None = None,
    ) -> list[dict]:
        """
        Fetch articles for all configured categories.
        Returns a flat merged list of raw article dicts.
        """
        categories = categories or _DEFAULT_CATEGORIES
        all_results: list[dict] = []
        for cat in categories:
            raw = self.fetch_by_category(cat)
            all_results.extend(raw)
        return all_results

    def upsert_articles(self, db: Session, raw_articles: list[dict]) -> int:
        """
        Map and insert new articles, skipping duplicates by newsdata_id and url.
        Returns the number of newly inserted articles.
        """
        if not self._api_key:
            logger.warning("NEWSDATA_API_KEY is not set — skipping upsert.")
            return 0

        # Build lookup sets for fast dedup check
        existing_newsdata_ids: set[str] = {
            row[0]
            for row in db.query(News.newsdata_id).filter(News.newsdata_id.isnot(None)).all()
        }
        existing_urls: set[str] = {
            row[0]
            for row in db.query(News.url).filter(News.url.isnot(None)).all()
        }

        inserted = 0
        for raw in raw_articles:
            newsdata_id = raw.get("article_id")
            url = raw.get("link")

            # Skip duplicates
            if newsdata_id and newsdata_id in existing_newsdata_ids:
                continue
            if url and url in existing_urls:
                continue

            kwargs = _map_article(raw)
            if not kwargs["title"]:
                continue
            if not kwargs["content"]:
                continue  # title is required

            article = News(**kwargs)
            db.add(article)
            db.flush()  # get article_id before we can summarize

            # Generate summary via Ollama (at scrape time)
            article.summary = generate_summary(kwargs.get("content"), kwargs.get("title"))
            if article.summary:
                article.embedding = embedder.embed_text(article.summary)

            # Only save article if summary was successfully generated
            if not article.summary:
                db.rollback()
                logger.warning("Skipped article '%s' — summarization failed", kwargs.get("title"))
                continue

            if newsdata_id:
                existing_newsdata_ids.add(newsdata_id)
            if url:
                existing_urls.add(url)

            inserted += 1

        if inserted:
            db.commit()
            logger.info("Upserted %d new articles", inserted)

        return inserted
