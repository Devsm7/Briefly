"""Auth business logic — user creation and login."""

from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate


class AuthService:
    """Handles all authentication-related database operations."""

    def register_user(self, db: Session, payload: UserCreate) -> User:
        """Create a new User. Raises ValueError if username already exists."""
        if db.query(User).filter(User.username == payload.username).first():
            raise ValueError("A user with this username already exists")

        user = User(
            username=payload.username,
            first_name=payload.first_name,
            last_name=payload.last_name,
            gender=payload.gender,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def authenticate_user(self, db: Session, username: str) -> User | None:
        """Find user by username. Returns User if found, else None."""
        return db.query(User).filter(User.username == username).first()


auth_service = AuthService()
