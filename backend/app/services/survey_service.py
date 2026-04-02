"""Survey business logic — save / retrieve survey preferences."""

from sqlalchemy.orm import Session

from app.models.survey import SurveyPreference
from app.schemas.survey import SurveySubmit

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


class SurveyService:

    def get_survey(self, db: Session, user_id: int) -> SurveyPreference | None:
        """Return the SurveyPreference for the given user, or None."""
        return db.query(SurveyPreference).filter(SurveyPreference.user_id == user_id).first()

    def upsert_survey(self, db: Session, user_id: int, payload: SurveySubmit) -> SurveyPreference:
        """Create or update a SurveyPreference. Derives interest_vector from Likert scores."""
        interest_vector = _build_interest_vector(payload.categories, payload.answers)

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

        db.commit()
        db.refresh(survey)
        return survey

    def skip_survey(self, db: Session, user_id: int) -> SurveyPreference:
        """Create a minimal record so user can proceed without completing the survey."""
        survey = db.query(SurveyPreference).filter(SurveyPreference.user_id == user_id).first()
        if survey:
            return survey

        survey = SurveyPreference(
            user_id=user_id,
            categories=[],
            answers={},
            interest_vector={},
            survey_completed=0,
        )
        db.add(survey)
        db.commit()
        db.refresh(survey)
        return survey


survey_service = SurveyService()
