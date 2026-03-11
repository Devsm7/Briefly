"""Pydantic schemas for User — request bodies and response shapes."""

# TODO: Import BaseModel, EmailStr from pydantic
# TODO: Import Optional, datetime from typing / datetime


class UserCreate:
    """Payload for POST /auth/register."""
    # TODO: email: EmailStr
    # TODO: password: str
    # TODO: full_name: Optional[str] = None
    pass


class UserLogin:
    """Payload for POST /auth/login."""
    # TODO: email: EmailStr
    # TODO: password: str
    pass


class UserOut:
    """Public user representation returned by the API."""
    # TODO: id, email, full_name, is_active, created_at
    # TODO: model_config = {"from_attributes": True}
    pass


class Token:
    """JWT token response."""
    # TODO: access_token: str
    # TODO: token_type: str = "bearer"
    pass


class PasswordResetRequest:
    """Payload for POST /auth/reset-password."""
    # TODO: email: EmailStr
    pass


class PasswordResetConfirm:
    """Payload for POST /auth/reset-password/confirm."""
    # TODO: token: str
    # TODO: new_password: str
    pass


class UserUpdate:
    """Payload for PATCH /users/me."""
    # TODO: full_name: Optional[str] = None
    pass
