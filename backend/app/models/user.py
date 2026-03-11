"""User SQLAlchemy ORM model — maps to the `users` table."""

# TODO: Import Column types, relationship, func from sqlalchemy
# TODO: Import Base from app.db.base


class User:
    """
    Represents an application user.

    Table: users
    Columns:
        id              - primary key
        email           - unique, indexed, not null
        hashed_password - bcrypt hash, not null
        full_name       - optional display name
        is_active       - soft-delete flag (default True)
        reset_token     - password reset token (nullable)
        reset_token_expires - token expiry datetime (nullable)
        created_at      - server default now()
        updated_at      - auto-updated on row change
    Relationships:
        survey          - one-to-one → SurveyPreference
        interactions    - one-to-many → UserInteraction
    """

    # TODO: Add __tablename__ = "users"
    # TODO: Define all Column fields
    # TODO: Define relationships
    pass
