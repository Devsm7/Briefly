"""Auth business logic — user creation, login validation, password reset."""

import secrets
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate


class AuthService:
    """Handles all authentication-related database operations."""

    def register_user(self, db: Session, payload: UserCreate) -> User:
        """
        Create a new User from UserCreate payload.
        Raises ValueError if email or username already exists.
        """
        if db.query(User).filter(User.email == payload.email).first():
            raise ValueError("A user with this email already exists")
        if db.query(User).filter(User.username == payload.username).first():
            raise ValueError("A user with this username already exists")

        user = User(
            email=payload.email,
            username=payload.username,
            full_name=payload.full_name,
            hashed_password=get_password_hash(payload.password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def authenticate_user(self, db: Session, identifier: str, password: str) -> User | None:
        """
        Verify identifier (email or username) + password.
        Returns User if valid, else None.
        """
        user = db.query(User).filter(User.email == identifier).first()
        if not user:
            user = db.query(User).filter(User.username == identifier).first()
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    def create_reset_token(self, db: Session, email: str) -> str:
        """
        Generate a 64-char random reset token, store in User row.
        Token expires 30 minutes from now.
        Returns the plain token.
        """
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise ValueError("No user with that email address")
        token = secrets.token_hex(32)
        user.reset_token = token
        user.reset_token_expires = datetime.now(timezone.utc) + timedelta(minutes=30)
        db.commit()
        return token

    def reset_password(self, db: Session, token: str, new_password: str) -> None:
        """
        Validate token and expiry, update hashed_password, clear token.
        Raises ValueError if token invalid or expired.
        """
        user = db.query(User).filter(User.reset_token == token).first()
        if not user or user.reset_token_expires is None:
            raise ValueError("Invalid or expired reset token")
        expires = user.reset_token_expires
        if expires.tzinfo is None:
            expires = expires.replace(tzinfo=timezone.utc)
        if datetime.now(timezone.utc) > expires:
            raise ValueError("Reset token has expired")
        user.hashed_password = get_password_hash(new_password)
        user.reset_token = None
        user.reset_token_expires = None
        db.commit()


auth_service = AuthService()
