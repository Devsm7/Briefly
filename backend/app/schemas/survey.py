"""Pydantic schemas for onboarding survey."""

# TODO: Import BaseModel from pydantic
# TODO: Import Optional, List, Dict, datetime


class SurveyCreate:
    """Payload for POST /survey."""
    # TODO: categories: List[str]   e.g. ["tech", "business"]
    # TODO: frequency: Optional[str] = None
    # TODO: preferred_sources: Optional[List[str]] = []
    pass


class SurveyOut:
    """Survey preference as returned by GET /survey."""
    # TODO: id, user_id, categories, frequency, preferred_sources,
    #       interest_vector, survey_completed, created_at
    # TODO: model_config = {"from_attributes": True}
    pass
