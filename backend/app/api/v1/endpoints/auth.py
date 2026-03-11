"""Auth endpoints: register, login, password reset."""

# TODO: Import APIRouter, Depends, HTTPException, status from fastapi
# TODO: Import Session from sqlalchemy.orm
# TODO: Import get_db from app.api.deps
# TODO: Import auth_service, user schemas

router = None  # TODO: router = APIRouter(prefix="/auth", tags=["auth"])


def register():
    """
    POST /auth/register
    Create a new user account.
    - Reject duplicate emails (HTTP 400)
    - Hash password before storing
    - Return UserOut
    """
    # TODO: implement
    raise NotImplementedError


def login():
    """
    POST /auth/login
    Authenticate and return a JWT access token.
    - Verify email exists and password matches hash
    - Return Token schema
    """
    # TODO: implement
    raise NotImplementedError


def request_password_reset():
    """
    POST /auth/reset-password
    Generate a reset token, store it in DB, log/email to user.
    Token expires in 30 minutes.
    """
    # TODO: implement
    raise NotImplementedError


def confirm_password_reset():
    """
    POST /auth/reset-password/confirm
    Validate reset token, update hashed_password, clear token.
    """
    # TODO: implement
    raise NotImplementedError
