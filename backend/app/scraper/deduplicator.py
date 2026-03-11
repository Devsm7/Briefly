"""Deduplication — prevent inserting articles already in the database."""

# TODO: Import Article model, Session


class Deduplicator:
    """Checks article URLs against existing url_hash values in the database."""

    def is_duplicate(self, db, url: str) -> bool:
        """
        Return True if an article with the same URL hash already exists in DB.
        Uses Article.make_hash(url) for comparison.
        """
        # TODO: compute hash; query Article by url_hash; return bool
        raise NotImplementedError

    def filter_new(self, db, articles: list[dict]) -> list[dict]:
        """
        Given a list of article dicts (each with a 'url' key),
        return only those whose URL hash is NOT already in the DB.
        More efficient than checking one-by-one for large batches.
        """
        # TODO: bulk-fetch existing hashes; set-difference; return filtered list
        raise NotImplementedError
