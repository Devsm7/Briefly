"""Generates master daily digest across all user topic categories."""

# TODO: Import Summarizer, NewsService, SurveyPreference, Article models
# TODO: Import datetime


class DigestBuilder:
    """Assembles a personalized daily digest for a user."""

    def build_digest(self, db, user_id: int) -> dict:
        """
        Build the daily digest for a user:
          1. Load user's preferred categories from SurveyPreference
          2. For each category, fetch the top 3 most recent articles
          3. Summarize each article (use cached summary if available)
          4. Assemble into a structured digest dict:
             {
               "date": "2024-01-15",
               "sections": [
                 {
                   "category": "tech",
                   "articles": [
                     {"title": ..., "summary": ..., "url": ..., "source": ...},
                     ...
                   ]
                 }
               ]
             }
          5. Return digest dict
        """
        # TODO: implement
        raise NotImplementedError

    def is_stale(self, last_generated_at) -> bool:
        """
        Return True if the digest is older than 24 hours and should be regenerated.
        """
        # TODO: compare last_generated_at to datetime.utcnow()
        raise NotImplementedError
