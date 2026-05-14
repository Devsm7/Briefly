"""Rank articles by interest alignment AND recency."""

from datetime import datetime, timezone

import numpy as np


class Ranker:
    # Tunable parameters — adjust to taste
    # Half-life in hours: articles lose half their recency score after this long
    RECENCY_HALF_LIFE_HOURS: float = 24.0
    # Balance weight: 0.0 = pure interest, 1.0 = pure recency
    TIME_BOOST: float = 0.20

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

    def _interest_score(
        self,
        article,
        user_embedding,
        interest_vector: dict[str, float],
        topic_keywords: list[str] | None = None,
    ) -> float:
        category_weight = interest_vector.get(getattr(article, "category", ""), 0.5)
        embedding = getattr(article, "embedding", None)

        if embedding and user_embedding is not None:
            semantic = self.cosine_similarity(embedding, user_embedding)
            base = semantic * category_weight
        elif interest_vector:
            base = category_weight
        else:
            base = 0.5

        # Keyword boost: cosine diff within same category is ~0.05 — too small to overcome
        # recency. Explicit keyword match on user-selected subtopics is reliable.
        if topic_keywords:
            text = (
                (getattr(article, "title", "") or "") + " " +
                (getattr(article, "summary", "") or "")
            ).lower()
            if any(term in text for term in topic_keywords):
                base = min(1.0, base + 0.25)

        return base

    def rank_articles(
        self,
        articles: list,
        user_embedding,
        interest_vector: dict[str, float],
        top_k: int = 20,
        topic_keywords: list[str] | None = None,
    ) -> list:
        """
        Rank articles by balancing interest alignment and recency.

        final_score = (1 - TIME_BOOST) × interest_score + TIME_BOOST × recency_score
        """
        scored = []
        for article in articles:
            interest = self._interest_score(article, user_embedding, interest_vector, topic_keywords)
            recency = self._recency_score(article)
            score = (1 - self.TIME_BOOST) * interest + self.TIME_BOOST * recency
            scored.append((score, article))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [article for _, article in scored[:top_k]]
