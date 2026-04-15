"""Pydantic schemas for onboarding survey."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, field_validator


class SurveySubmit(BaseModel):
    """Payload for POST /survey — full survey submission."""
    categories: List[str]
    answers: Dict[str, Any]

    @field_validator("categories")
    @classmethod
    def categories_valid(cls, v: List[str]) -> List[str]:
        allowed = {"tech", "politics", "sport"}
        invalid = [c for c in v if c not in allowed]
        if invalid:
            raise ValueError(f"Invalid categories: {invalid}. Allowed: {allowed}")
        return v


class SurveyOut(BaseModel):
    """Survey preference as returned by the API."""
    id: int
    user_id: int
    categories: List[str]
    answers: Dict[str, Any]
    interest_vector: Dict[str, float]
    survey_completed: int
    created_at: datetime

    model_config = {"from_attributes": True}
