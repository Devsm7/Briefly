"""Pydantic schemas for User — request bodies and response shapes."""

import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator


class UserCreate(BaseModel):
    """Payload for POST /auth/register."""
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None

    @field_validator("username")
    @classmethod
    def username_valid(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters")
        if len(v) > 50:
            raise ValueError("Username must be at most 50 characters")
        if not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError("Username may only contain letters, numbers, and underscores")
        return v

    @field_validator("full_name")
    @classmethod
    def full_name_valid(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip()
            if len(v) > 100:
                raise ValueError("Full name must be at most 100 characters")
            if len(v) == 0:
                return None
        return v


class UserLogin(BaseModel):
    """Payload for POST /auth/login. Accepts email or username as identifier."""
    identifier: str
    password: str


class UserOut(BaseModel):
    """Public user representation returned by the API."""
    id: int
    email: str
    username: str
    full_name: Optional[str] = None
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"


class PasswordResetRequest(BaseModel):
    """Payload for POST /auth/reset-password."""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Payload for POST /auth/reset-password/confirm."""
    token: str
    new_password: str


class UserUpdate(BaseModel):
    """Payload for PATCH /users/me."""
    full_name: Optional[str] = None
