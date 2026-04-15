"""Survey business logic — save / retrieve survey preferences.

On upsert, data is written to TWO tables:
  - survey_preferences  → tracks survey_completed flag + raw data
  - user_interest_profiles → keywords (raw answers) + interests_vector (weights)
"""

import logging

from sqlalchemy.orm import Session

from app.models.survey import SurveyPreference
from app.models.user_interest_profile import UserInterestProfile
from app.schemas.survey import SurveySubmit

logger = logging.getLogger(__name__)

# Likert answer keys per category — used to build interest_vector
_LIKERT_KEYS = {"tech": "Q05", "politics": "Q08", "sport": "Q14"}


def _build_interest_vector(categories: list[str], answers: dict) -> dict[str, float]:
    """Derive category weights from Likert scores (1-5) normalized to 0.0-1.0."""
    vector: dict[str, float] = {}
    for cat in categories:
        key = _LIKERT_KEYS.get(cat)
        score = answers.get(key) if key else None
        vector[cat] = round(int(score) / 5.0, 2) if score is not None else 0.5
    return vector


def _upsert_interest_profile(
    db: Session,
    user_id: int,
    keywords: list[str],
    interests_vector: list[str],
) -> UserInterestProfile:
    """Create or update the user_interest_profiles row for the given user."""
    profile = (
        db.query(UserInterestProfile)
        .filter(UserInterestProfile.user_id == user_id)
        .first()
    )
    if profile:
        profile.keywords = keywords
        profile.interests_vector = interests_vector
    else:
        profile = UserInterestProfile(
            user_id=user_id,
            keywords=keywords,
            interests_vector=interests_vector,
        )
        db.add(profile)
    return profile


class SurveyService:

    def get_survey(self, db: Session, user_id: int) -> SurveyPreference | None:
        """Return the SurveyPreference for the given user, or None."""
        return db.query(SurveyPreference).filter(SurveyPreference.user_id == user_id).first()

    def upsert_survey(self, db: Session, user_id: int, payload: SurveySubmit) -> SurveyPreference:
        """Create or update survey data.

        Writes to both tables in a single transaction:
          - survey_preferences: categories, answers, interest_vector, survey_completed
          - user_interest_profiles: keywords (answers), interests_vector
        """
        interest_vector = _build_interest_vector(payload.categories, payload.answers)

        # ── survey_preferences ──────────────────────────────────────────────
        survey = db.query(SurveyPreference).filter(SurveyPreference.user_id == user_id).first()
        if survey:
            survey.categories = payload.categories
            survey.answers = payload.answers
            survey.interest_vector = interest_vector
            survey.survey_completed = 1
        else:
            survey = SurveyPreference(
                user_id=user_id,
                categories=payload.categories,
                answers=payload.answers,
                interest_vector=interest_vector,
                survey_completed=1,
            )
            db.add(survey)

        # ── user_interest_profiles ───────────────────────────────────────────
        try:
            logger.info("[survey] Writing to user_interest_profiles for user_id=%s", user_id)
            
            # Convert dict to array of "key:value" strings for TEXT[] column
            keys_list = [f"{k}:{v}" for k, v in payload.answers.items()]
            vecs_list = [f"{k}:{v}" for k, v in interest_vector.items()]

            _upsert_interest_profile(
                db,
                user_id=user_id,
                keywords=keys_list,
                interests_vector=vecs_list,
            )
            logger.info("[survey] user_interest_profiles write succeeded for user_id=%s", user_id)
        except Exception as exc:
            logger.error(
                "[survey] FAILED to write user_interest_profiles for user_id=%s: %s",
                user_id, exc, exc_info=True,
            )
            db.rollback()
            raise

        db.commit()
        db.refresh(survey)
        return survey

    def skip_survey(self, db: Session, user_id: int) -> SurveyPreference:
        """Create minimal records so user can proceed without completing the survey."""
        survey = db.query(SurveyPreference).filter(SurveyPreference.user_id == user_id).first()
        if not survey:
            survey = SurveyPreference(
                user_id=user_id,
                categories=[],
                answers={},
                interest_vector={},
                survey_completed=0,
            )
            db.add(survey)

        # Ensure interest profile row exists even if survey is skipped
        try:
            logger.info("[survey] Writing empty user_interest_profiles for user_id=%s (skip)", user_id)
            _upsert_interest_profile(db, user_id=user_id, keywords=[], interests_vector=[])
        except Exception as exc:
            logger.error(
                "[survey] FAILED to write user_interest_profiles on skip for user_id=%s: %s",
                user_id, exc, exc_info=True,
            )
            db.rollback()
            raise

        db.commit()
        db.refresh(survey)
        return survey


survey_service = SurveyService()
