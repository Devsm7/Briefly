"""DB initializer — create tables on first run (dev convenience)."""

from app.db.base import Base
from app.db.session import engine


def init_db():
    """
    Create all tables that don't yet exist.
    Use only in development; prefer Alembic migrations in production.
    """
    Base.metadata.create_all(bind=engine)
