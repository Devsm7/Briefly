"""News article business logic — querying feed, trending, and library."""

# TODO: Import Session, Article, UserInteraction models


class NewsService:
    """Database operations for the news feed and article queries."""

    def get_feed(self, db, category=None, page: int = 1, per_page: int = 20):
        """
        Return a paginated list of articles, optionally filtered by category.
        Orders by published_at descending.
        Returns (articles: List[Article], total: int).
        """
        # TODO: implement
        raise NotImplementedError

    def get_article_by_id(self, db, article_id: int):
        """
        Return a single Article by primary key.
        Raises HTTP 404 if not found.
        """
        # TODO: implement
        raise NotImplementedError

    def get_trending(self, db, hours: int = 24, limit: int = 20):
        """
        Return articles ordered by number of interactions in the last `hours`.
        """
        # TODO: aggregate user_interactions, filter created_at > now - hours
        raise NotImplementedError

    def get_library(self, db, user_id: int):
        """
        Return all articles bookmarked (action='save') by the given user.
        """
        # TODO: join news on user_interactions WHERE user_id AND action='save'
        raise NotImplementedError
