"""Rank articles by cosine similarity to the user's interest vector."""

import numpy as np


class Ranker:
    """Scores and sorts articles against a user's interest profile."""

    def cosine_similarity(self, vec_a: list[float], vec_b: list[float]) -> float:
        """
        Compute cosine similarity between two equal-length vectors.
        Returns a float in [-1.0, 1.0].
        """
        a = np.array(vec_a, dtype=np.float32)
        b = np.array(vec_b, dtype=np.float32)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(a, b) / (norm_a * norm_b))

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
        raise NotImplementedError
