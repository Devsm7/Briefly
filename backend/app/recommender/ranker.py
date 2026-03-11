"""Rank articles by cosine similarity to the user's interest vector."""

# TODO: Import numpy as np
# TODO: Import Article, SurveyPreference models


class Ranker:
    """Scores and sorts articles against a user's interest profile."""

    def cosine_similarity(self, vec_a: list[float], vec_b: list[float]) -> float:
        """
        Compute cosine similarity between two equal-length vectors.
        Returns a float in [-1.0, 1.0].
        """
        # TODO: np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
        raise NotImplementedError

    def rank_articles(
        self,
        articles: list,
        interest_vector: dict[str, float],
        top_k: int = 20,
    ) -> list:
        """
        Score each article by cosine similarity between its embedding
        and the user's interest_vector converted to an embedding-space query.
        Returns the top_k articles sorted by score descending.

        Fallback: if an article has no embedding, score by category weight match.
        """
        # TODO: implement scoring and sorting
        raise NotImplementedError
