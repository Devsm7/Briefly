"""Rank articles by interest alignment AND recency."""

from datetime import datetime, timezone

import numpy as np


class Ranker:
    # Tunable parameters — adjust to taste
    # Half-life in hours: articles lose half their recency score after this long
    RECENCY_HALF_LIFE_HOURS: float = 24.0
    # Balance weight: 0.0 = pure interest, 1.0 = pure recency
    TIME_BOOST: float = 0.35

    def cosine_similarity(self, vec_a: list[float], vec_b: list[float]) -> float:
        a = np.array(vec_a)
        b = np.array(vec_b)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    def _recency_score(self, article) -> float:
        """
        Exponential-decay recency score (0-1).

        Score = exp(-λ × age_hours) where λ = ln(2) / half_life_hours.
        Falls back to created_at (DB insertion time) when published_date is unavailable.
        """
        decay_lambda = 0.693147 / self.RECENCY_HALF_LIFE_HOURS  # ln(2) / half_life

        # Prefer published_date; fall back to created_at
        date_str = getattr(article, "published_date", None)
        if date_str:
            try:
                # NewsData.io publishes ISO-8601 strings like "2026-05-07T14:30:00Z"
                pub = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            except (ValueError, AttributeError):
                pub = None
        else:
            pub = None

        if pub is None:
            pub = getattr(article, "created_at", None)

        if pub is None:
            return 0.0  # No date at all — treat as very old

        # Ensure tz-aware
        if pub.tzinfo is None:
            pub = pub.replace(tzinfo=timezone.utc)
        age_hours = (datetime.now(timezone.utc) - pub).total_seconds() / 3600
        return float(max(0.0, np.exp(-decay_lambda * age_hours)))

    def _interest_score(self, article, user_embedding, interest_vector: dict[str, float]) -> float:
        """
        Combined semantic + category interest score (0-1).

        - If user_embedding is available AND article has embedding → cosine similarity × category_weight
        - If user_embedding is None but interest_vector has weights → use category_weight only
          (survey-only ranking, used for new users with no likes)
        - If neither → neutral 0.5
        """
        category_weight = interest_vector.get(getattr(article, "category", ""), 0.5)
        embedding = getattr(article, "embedding", None)

        if embedding and user_embedding is not None:
            semantic = self.cosine_similarity(embedding, user_embedding)
            return semantic * category_weight

        if interest_vector:  # survey exists but no embedding yet
            return category_weight

        return 0.5  # no survey, no embedding — neutral

    def rank_articles(
        self,
        articles: list,
        user_embedding,
        interest_vector: dict[str, float],
        top_k: int = 20,
    ) -> list:
        """
        Rank articles by balancing interest alignment and recency.

        final_score = (1 - TIME_BOOST) × interest_score + TIME_BOOST × recency_score
        """
        scored = []
        for article in articles:
            interest = self._interest_score(article, user_embedding, interest_vector)
            recency = self._recency_score(article)
            score = (1 - self.TIME_BOOST) * interest + self.TIME_BOOST * recency
            scored.append((score, article))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [article for _, article in scored[:top_k]]
