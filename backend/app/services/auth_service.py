"""Auth business logic — user creation, login validation, password reset."""

# TODO: Import Session, User model, security helpers, schemas


class AuthService:
    """Handles all authentication-related database operations."""

    def register_user(self, db, payload):
        """
        Create a new User from UserCreate payload.
        Raises ValueError if email already exists.
        Returns the new User ORM object.
        """
        # TODO: check duplicate email → raise
        # TODO: hash password
        # TODO: insert User → commit → refresh → return
        raise NotImplementedError

    def authenticate_user(self, db, email: str, password: str):
        """
        Verify email/password. Returns User if valid, else None.
        """
        # TODO: query User by email
        # TODO: verify_password(password, user.hashed_password)
        raise NotImplementedError

    def create_reset_token(self, db, email: str) -> str:
        """
        Generate a 32-char random reset token, store in User row.
        Token expires 30 minutes from now.
        Returns the plain token (log/email it to the user).
        """
        # TODO: implement
        raise NotImplementedError

    def reset_password(self, db, token: str, new_password: str):
        """
        Validate token and expiry, update hashed_password, clear token.
        Raises ValueError if token invalid or expired.
        """
        # TODO: implement
        raise NotImplementedError
