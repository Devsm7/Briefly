"""Text cleaning utilities — strip HTML, normalize whitespace, remove junk."""

# TODO: Import re, BeautifulSoup from bs4


class Cleaner:
    """Cleans raw scraped text before it is stored in the database."""

    def clean_text(self, raw: str) -> str:
        """
        Given raw HTML or plain text, return clean readable text:
          - Strip all HTML tags via BeautifulSoup
          - Remove special characters and excessive whitespace
          - Normalize Unicode
        Returns None if the result is empty (caller should discard article).
        """
        # TODO: BeautifulSoup(raw, "lxml").get_text()
        # TODO: re.sub to remove non-printable chars
        # TODO: strip and collapse whitespace
        raise NotImplementedError

    def is_valid(self, article: dict) -> bool:
        """
        Return True only if all required fields are non-null and non-empty:
        title, description, url, published_at.
        Articles failing this check are discarded before DB insertion.
        """
        # TODO: check required fields
        raise NotImplementedError
