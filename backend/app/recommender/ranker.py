"""Rank articles by cosine similarity to the user's interest vector."""

import numpy as np


class Ranker:
    """Scores and sorts articles against a user's interest profile."""

    def cosine_similarity(self, vec_a: list[float], vec_b: list[float]) -> float:
        """
        Compute cosine similarity between two equal-length vectors.
        Returns a float in [-1.0, 1.0].
        """
        a = np.array(vec_a)
        b = np.array(vec_b)
        return float(np.dot(a,b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    def rank_articles(
        self,
        articles: list,
        user_embedding,
        interest_vector: dict[str, float],
        top_k: int = 20,
    ) -> list:
        """
        Score each article by cosine similarity between its embedding
        and the user's interest_vector converted to an embedding-space query.
        Returns the top_k articles sorted by score descending.

        Fallback: if an article has no embedding, score by category weight match.
        """
        scored =[]
        for article in articles:
            category_weight = interest_vector.get(article.category, 0.5) 
            if article.embedding:
                semantic_score = self.cosine_similarity(article.embedding, user_embedding)
            else:
                semantic_score = 0.0
            score = semantic_score * category_weight
            scored.append((score,article))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [article for _, article in scored[:top_k]]
