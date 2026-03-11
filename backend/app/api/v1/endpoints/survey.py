"""Onboarding survey endpoints."""

# TODO: Import APIRouter, Depends from fastapi
# TODO: Import get_current_user, get_db, survey_service

router = None  # TODO: router = APIRouter(prefix="/survey", tags=["survey"])


def get_survey():
    """
    GET /survey
    Return the current user's survey preferences.
    If no survey exists, return 404.
    """
    # TODO: implement
    raise NotImplementedError


def submit_survey():
    """
    POST /survey
    Save or update the user's onboarding survey answers.
    - Store categories, frequency, preferred_sources
    - Trigger interest_vector generation from categories
    - Return SurveyOut
    """
    # TODO: implement
    raise NotImplementedError


def skip_survey():
    """
    POST /survey/skip
    Create a minimal SurveyPreference record with survey_completed=0.
    Allows user to proceed without filling out the survey.
    """
    # TODO: implement
    raise NotImplementedError
