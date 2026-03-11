"""Article SQLAlchemy ORM model — maps to the `news` table."""

# TODO: Import Column types, relationship, func from sqlalchemy
# TODO: Import Base from app.db.base
# TODO: Import hashlib for make_hash()


class Article:
    """
    Scraped news article.

    Table: news
    Columns:
        id           - primary key
        url_hash     - SHA-256 of URL (unique, indexed) — used for deduplication
        title        - article headline (max 512 chars)
        description  - short excerpt
        content      - full body text (nullable)
        url          - canonical article URL
        source       - publisher name (e.g. "TechCrunch")
        category     - "tech" | "business" | "politics" | "sports"
        published_at - publication datetime
        summary      - 3-5 bullet LLM-generated summary (nullable)
        embedding    - JSON array of floats from sentence-transformers
        created_at   - server default now()
    Relationships:
        interactions - one-to-many → UserInteraction
    """

    # TODO: Add __tablename__ = "news"
    # TODO: Define all Column fields
    # TODO: Define relationships

    @staticmethod
    def make_hash(url: str) -> str:
        """Return SHA-256 hex digest of the given URL for deduplication."""
        # TODO: import hashlib; return hashlib.sha256(url.encode()).hexdigest()
        raise NotImplementedError
