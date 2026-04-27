"""User profile endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.survey import SurveyOut
from app.schemas.user import UserOut, UserUpdate
from app.services.survey_service import survey_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    """GET /users/me — Return the current authenticated user's profile."""
    return current_user


@router.get("/me/with-survey")
def get_me_with_survey(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """GET /users/me/with-survey — Return user profile plus their survey/interests data."""
    survey = survey_service.get_survey(db, current_user.id)
    return {
        "user": UserOut.model_validate(current_user),
        "survey": SurveyOut.model_validate(survey) if survey else None,
    }


@router.patch("/me", response_model=UserOut)
def update_me(
    payload: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """PATCH /users/me — Update profile fields."""
    if payload.first_name is not None:
        current_user.first_name = payload.first_name
    if payload.last_name is not None:
        current_user.last_name = payload.last_name
    if payload.gender is not None:
        current_user.gender = payload.gender
    db.commit()
    db.refresh(current_user)
    return current_user
