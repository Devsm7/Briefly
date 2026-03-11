"""Build and update the user interest vector from survey and feedback signals."""

# TODO: Import numpy, SurveyPreference, UserInteraction, Article models
# Category ordering (index) used in the vector:
# CATEGORIES = ["tech", "business", "politics", "sports"]


class InterestVector:
    """Computes and maintains a per-user interest profile vector."""

    def build_from_survey(self, categories: list[str]) -> dict[str, float]:
        """
        Create an initial interest_vector dict from onboarding survey answers.
        Selected categories get equal weight; unselected get near-zero weight.
        Example → {"tech": 0.5, "business": 0.5, "politics": 0.0, "sports": 0.0}
        """
        # TODO: distribute weight equally among selected categories
        raise NotImplementedError

    def update_from_feedback(
        self,
        current_vector: dict[str, float],
        article_category: str,
        action: str,
    ) -> dict[str, float]:
        """
        Re-weight the interest vector based on a single feedback action.
        - "like" / "more_like_this"  → increase category weight by delta
        - "dislike" / "less_like_this" → decrease category weight by delta
        Normalize the resulting weights so they sum to 1.0.
        """
        # TODO: define DELTA = 0.05
        # TODO: adjust, clamp to [0.0, 1.0], normalize
        raise NotImplementedError

    def save_to_db(self, db, user_id: int, vector: dict[str, float]):
        """Persist the updated interest_vector JSON to SurveyPreference."""
        # TODO: update SurveyPreference.interest_vector for user_id
        raise NotImplementedError
