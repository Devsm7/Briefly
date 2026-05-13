"""Survey business logic — save / retrieve survey preferences.

Data is written to survey_preferences (always).  Optionally to user_interest_profiles
when that table exists and the migration has been applied.

───────────────────────────────────────────────────────────────────────────────
NOTE ON EMBEDDINGS (not yet implemented):
  The interest_vector stored here is derived from survey Likert scores — it is NOT
  yet connected to article embeddings.

  Once recommender/embedder.py is live:
    - Articles get 384-dim vectors stored in News.embedding (background job)
    - recommender/ranker.py (Ranker class) uses cosine similarity between
      News.embedding and the user's interest_vector to rank articles
    - agent_service.py (_get_personalized_recommendations) will call ranker.rank_articles()
      instead of the current category-weight fallback
    - recommender/interest_vector.py (InterestVector class) will update interest_vector
      based on UserInteraction rows (read/like/dislike signals)

  user_interest_profiles table (not yet migrated) will store:
    - keywords: raw answer keys from survey
    - interests_vector: category weight strings (e.g. "tech:0.8")
───────────────────────────────────────────────────────────────────────────────
"""

import logging

from sqlalchemy.orm import Session

from app.models.survey import SurveyPreference

# Import removed — user_interest_profiles table not yet migrated.
# Uncomment when the table migration has been applied and embeddings pipeline is live.
# from app.models.user_interest_profile import UserInterestProfile

from app.schemas.survey import SurveySubmit

logger = logging.getLogger(__name__)

# Likert answer keys per category — used to build interest_vector from survey answers
_LIKERT_KEYS = {
    "tech": "Q05",
    "politics": "Q08",
    "sport": "Q14",
    "business": "Q18",
    "health": "Q21",
    "science": "Q24",
}


def _build_interest_vector(categories: list[str], answers: dict) -> dict[str, float]:
    """
    Derive category weights from Likert scores (1-5) normalized to 0.0-1.0.
    This is the initial interest_vector — not yet powered by embeddings.
    """
    vector: dict[str, float] = {}
    for cat in categories:
        key = _LIKERT_KEYS.get(cat)
        score = answers.get(key) if key else None
        vector[cat] = round(int(score) / 5.0, 2) if score is not None else 0.5
    return vector


# ── user_interest_profiles (table not yet migrated) ─────────────────────────


def _upsert_interest_profile(
    _db: Session,
    _user_id: int,
    _keywords: list[str],
    _interests_vector: list[str],
):
    """
    Create or update the user_interest_profiles row for the given user.
    Requires the user_interest_profiles table to exist (migration not yet applied).

    Fields:
      keywords   — "key:value" strings from raw survey answers
      interests_vector — "category:weight" strings from interest_vector dict

    Uncomment this function and the import above once the table migration exists.
    """
    # from app.models.user_interest_profile import UserInterestProfile
    #
    # profile = (
    #     _db.query(UserInterestProfile)
    #     .filter(UserInterestProfile.user_id == _user_id)
    #     .first()
    # )
    # if profile:
    #     profile.keywords = _keywords
    #     profile.interests_vector = _interests_vector
    # else:
    #     profile = UserInterestProfile(
    #         user_id=_user_id,
    #         keywords=_keywords,
    #         interests_vector=_interests_vector,
    #     )
    #     _db.add(profile)
    # return profile
    raise NotImplementedError("user_interest_profiles table not yet migrated")
    del _db, _user_id, _keywords, _interests_vector  # noqa: F841 — placeholder, never reached


# ──────────────────────────────────────────────────────────────────────────────


class SurveyService:

    def get_survey(self, db: Session, user_id: int) -> SurveyPreference | None:
        """Return the SurveyPreference for the given user, or None."""
        return db.query(SurveyPreference).filter(SurveyPreference.user_id == user_id).first()

    def upsert_survey(
        self, db: Session, user_id: int, payload: SurveySubmit
    ) -> SurveyPreference:
        """
        Create or update survey data for a user.

        Writes to survey_preferences (always).  Optionally writes to
        user_interest_profiles if that table exists (safely wrapped — won't
        error if the table hasn't been migrated yet).

        interest_vector is built from Likert scores.  When embeddings are live,
        the ranker will use cosine similarity between News.embedding and this
        vector instead of simple category weighting.
        """
        interest_vector = _build_interest_vector(payload.categories, payload.answers)

        # ── survey_preferences (always) ─────────────────────────────────────
        survey = db.query(SurveyPreference).filter(
            SurveyPreference.user_id == user_id
        ).first()
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

        # ── user_interest_profiles (safe — table may not exist yet) ─────────
        try:
            keys_list = [f"{k}:{v}" for k, v in payload.answers.items()]
            vecs_list = [f"{k}:{v}" for k, v in interest_vector.items()]
            _upsert_interest_profile(db, user_id, keys_list, vecs_list)
        except NotImplementedError:
            # Table not ready — survey_preferences write is sufficient
            pass
        except Exception as exc:
            logger.error(
                "[survey] Failed user_interest_profiles write for user_id=%s: %s",
                user_id, exc, exc_info=True,
            )
            # Don't rollback — survey_preferences already succeeded
            db.commit()

        # Invalidate cached embedding — regenerated on next recommendations request
        survey.user_embedding = None

        db.commit()
        db.refresh(survey)
        return survey

    def skip_survey(self, db: Session, user_id: int) -> SurveyPreference:
        """
        Create minimal records so user can proceed without completing the survey.
        Sets survey_completed=0 so the redirect-to-survey flow won't fire again.
        """
        survey = db.query(SurveyPreference).filter(
            SurveyPreference.user_id == user_id
        ).first()
        if not survey:
            survey = SurveyPreference(
                user_id=user_id,
                categories=[],
                answers={},
                interest_vector={},
                survey_completed=0,
            )
            db.add(survey)

        # user_interest_profiles write is safe — skips if table doesn't exist
        try:
            _upsert_interest_profile(db, user_id, [], [])
        except NotImplementedError:
            pass
        except Exception as exc:
            logger.error(
                "[survey] Failed user_interest_profiles write on skip for user_id=%s: %s",
                user_id, exc, exc_info=True,
            )
            db.commit()

        db.commit()
        db.refresh(survey)
        return survey


survey_service = SurveyService()