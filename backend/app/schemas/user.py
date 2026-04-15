"""Pydantic schemas for User — request bodies and response shapes."""

import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator


class UserCreate(BaseModel):
    """Payload for POST /auth/register."""
    username: str
    first_name: str
    last_name: str
    gender: Optional[str] = None

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

    @field_validator("gender")
    @classmethod
    def gender_valid(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip().lower()
            if v not in ("male", "female"):
                raise ValueError("Gender must be 'male' or 'female'")
        return v


class UserLogin(BaseModel):
    """Payload for POST /auth/login. Username only."""
    username: str


class UserOut(BaseModel):
    """Public user representation returned by the API."""
    id: int
    username: str
    first_name: str
    last_name: str
    gender: Optional[str] = None
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"


class UserUpdate(BaseModel):
    """Payload for PATCH /users/me."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
