"""Build and update the user interest vector from survey and feedback signals."""

_DELTA = 0.05


class InterestVector:
    """Computes and maintains a per-user interest profile vector."""

    def update_from_feedback(
        self,
        current_vector: dict[str, float],
        article_category: str,
        action: str,
    ) -> dict[str, float]:
        """
        Adjust the category weight for a single like/dislike action.
        Like → +0.05 (capped at 1.0), Dislike → -0.05 (floor 0.0).
        """
        vector = dict(current_vector)
        cat = (article_category or "").lower().strip()
        if not cat:
            return vector
        current = vector.get(cat, 0.5)
        if action in ("like", "more_like_this"):
            vector[cat] = min(1.0, current + _DELTA)
        elif action in ("dislike", "less_like_this"):
            vector[cat] = max(0.0, current - _DELTA)
        return vector

    def save_to_db(self, db, user_id: int, vector: dict[str, float]) -> None:
        """Persist the updated interest_vector to SurveyPreference."""
        from app.models.survey import SurveyPreference
        survey = db.query(SurveyPreference).filter(
            SurveyPreference.user_id == user_id
        ).first()
        if survey:
            survey.interest_vector = vector
            db.commit()


interest_vector_svc = InterestVector()
