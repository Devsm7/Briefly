"""SQLAlchemy synchronous session factory and get_db dependency."""

# TODO: Import sqlalchemy.create_engine, sessionmaker
# TODO: Create engine from settings.DATABASE_URL (pool_pre_ping=True)
# TODO: Create SessionLocal = sessionmaker(...)


def get_db():
    """FastAPI dependency — yields a DB session and closes it after request."""
    # TODO: open SessionLocal(), yield, finally close
    raise NotImplementedError
