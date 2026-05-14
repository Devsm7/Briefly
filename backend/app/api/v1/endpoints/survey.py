"""Onboarding survey endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.survey import SurveyOut, SurveySubmit
from app.services.survey_service import survey_service
from app.api.v1.endpoints.recommendations import invalidate_recs_cache

router = APIRouter(prefix="/survey", tags=["survey"])


@router.get("", response_model=SurveyOut)
def get_survey(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """GET /survey — Return the current user's survey preferences."""
    survey = survey_service.get_survey(db, current_user.id)
    if not survey:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Survey not found")
    return survey


@router.post("", response_model=SurveyOut, status_code=status.HTTP_201_CREATED)
def submit_survey(
    payload: SurveySubmit,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """POST /survey — Save or update the user's onboarding survey answers."""
    try:
        result = survey_service.upsert_survey(db, current_user.id, payload)
        invalidate_recs_cache(current_user.id)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.post("/skip", response_model=SurveyOut)
def skip_survey(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """POST /survey/skip — Skip the survey and proceed to dashboard."""
    result = survey_service.skip_survey(db, current_user.id)
    invalidate_recs_cache(current_user.id)
    return result
