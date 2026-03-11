"""Survey business logic — save / retrieve survey preferences."""

# TODO: Import Session, SurveyPreference model, interest_vector module


class SurveyService:
    """Database operations for onboarding survey preferences."""

    def get_survey(self, db, user_id: int):
        """
        Return the SurveyPreference for the given user, or None if not found.
        """
        # TODO: query SurveyPreference by user_id
        raise NotImplementedError

    def upsert_survey(self, db, user_id: int, payload):
        """
        Create or update a SurveyPreference from SurveyCreate payload.
        After saving, call interest_vector.build() to generate initial weights.
        Returns the saved SurveyPreference.
        """
        # TODO: upsert logic (check if exists → update; else create)
        # TODO: build interest_vector from categories
        # TODO: commit, refresh, return
        raise NotImplementedError

    def skip_survey(self, db, user_id: int):
        """
        Create a minimal SurveyPreference row with survey_completed=0.
        Allows users to proceed without completing the survey.
        """
        # TODO: insert minimal record with all defaults
        raise NotImplementedError
