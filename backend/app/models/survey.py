"""SurveyPreference ORM model — maps to the `survey_preferences` table."""

# TODO: Import Column types, ForeignKey, relationship, func from sqlalchemy
# TODO: Import Base from app.db.base


class SurveyPreference:
    """
    Stores onboarding survey answers and derived interest vector.

    Table: survey_preferences
    Columns:
        id                - primary key
        user_id           - FK → users.id (unique: one survey per user)
        categories        - JSON list of selected categories
                           e.g. ["tech", "business"]
        frequency         - preferred reading frequency
                           "morning" | "evening" | "both" | "realtime"
        preferred_sources - JSON list of preferred publisher names
        interest_vector   - JSON dict of category → weight floats
                           e.g. {"tech": 0.6, "business": 0.4}
        survey_completed  - 0 = skipped/partial, 1 = completed
        created_at        - server default now()
        updated_at        - auto-updated on change
    Relationships:
        user - many-to-one → User
    """

    # TODO: Add __tablename__ = "survey_preferences"
    # TODO: Define all Column fields
    # TODO: Define relationship back to User
    pass
