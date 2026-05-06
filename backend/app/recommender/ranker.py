"""Rank articles by cosine similarity to the user's interest vector."""

import numpy as np


class Ranker:
    def cosine_similarity(self, vec_a: list[float], vec_b: list[float]) -> float:
        a = np.array(vec_a)
        b = np.array(vec_b)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    def rank_articles(
        self,
        articles: list,
        user_embedding,
        interest_vector: dict[str, float],
        top_k: int = 20,
    ) -> list:
        scored = []
        for article in articles:
            category_weight = interest_vector.get(article.category, 0.5)
            if article.embedding:
                semantic_score = self.cosine_similarity(article.embedding, user_embedding)
            else:
                semantic_score = 0.0
            score = semantic_score * category_weight
            scored.append((score, article))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [article for _, article in scored[:top_k]]
