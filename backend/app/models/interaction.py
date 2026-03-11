"""UserInteraction ORM model — maps to the `user_interactions` table."""

# TODO: Import Column types, ForeignKey, relationship, func from sqlalchemy
# TODO: Import Base from app.db.base


class UserInteraction:
    """
    Records every user behavior signal against an article.

    Table: user_interactions
    Columns:
        id           - primary key
        user_id      - FK → users.id (indexed)
        article_id   - FK → news.id (indexed)
        action       - "view" | "like" | "dislike" | "save" | "unsave"
                      | "more_like_this" | "less_like_this"
        read_time    - seconds spent reading (nullable float)
        scroll_depth - fraction of article scrolled 0.0–1.0 (nullable float)
        created_at   - server default now()
    Relationships:
        user    - many-to-one → User
        article - many-to-one → Article
    """

    # TODO: Add __tablename__ = "user_interactions"
    # TODO: Define all Column fields
    # TODO: Define relationships to User and Article
    pass
