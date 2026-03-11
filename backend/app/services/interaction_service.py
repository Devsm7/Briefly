"""Interaction tracking business logic — log events and re-weight interest vector."""

# TODO: Import Session, UserInteraction, SurveyPreference models
# TODO: Import interest_vector module


class InteractionService:
    """Persists user behavior events and triggers interest vector updates."""

    def log_interaction(self, db, user_id: int, payload):
        """
        Insert a UserInteraction row from InteractionCreate payload.
        After insert, if action is 'like', 'dislike', 'more_like_this',
        or 'less_like_this', call interest_vector.update() to re-weight.
        Returns the created UserInteraction.
        """
        # TODO: implement
        raise NotImplementedError

    def get_user_interactions(self, db, user_id: int, article_id=None, action=None):
        """
        Return interaction records for a user, with optional filters
        for a specific article or action type.
        """
        # TODO: implement
        raise NotImplementedError
