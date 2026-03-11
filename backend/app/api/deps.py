"""Shared FastAPI dependencies — database session, current-user guard."""

# TODO: Import Depends, HTTPException, status from fastapi
# TODO: Import HTTPBearer, HTTPAuthorizationCredentials from fastapi.security
# TODO: Import Session from sqlalchemy.orm
# TODO: Import decode_token from app.core.security
# TODO: Import get_db from app.db.session
# TODO: Import User from app.models.user


def get_current_user():
    """
    FastAPI dependency.
    Validates the Bearer JWT in the Authorization header.
    Returns the authenticated User ORM object.
    Raises HTTP 401 if token is missing, invalid, or user is inactive.
    """
    # TODO:
    #   1. Extract token from HTTPBearer credentials
    #   2. decode_token(token) → payload or None
    #   3. If None → raise 401
    #   4. Query User by payload["sub"]
    #   5. If not found or not active → raise 401
    #   6. Return user
    raise NotImplementedError
