"""User profile endpoints."""

# TODO: Import APIRouter, Depends from fastapi
# TODO: Import get_current_user, get_db from app.api.deps

router = None  # TODO: router = APIRouter(prefix="/users", tags=["users"])


def get_me():
    """GET /users/me — Return the current authenticated user's profile."""
    # TODO: return current_user mapped to UserOut
    raise NotImplementedError


def update_me():
    """PATCH /users/me — Update full_name or other profile fields."""
    # TODO: apply UserUpdate payload to current_user; commit; return UserOut
    raise NotImplementedError
