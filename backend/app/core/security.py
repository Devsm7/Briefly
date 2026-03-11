"""JWT token creation/verification and bcrypt password hashing."""

# TODO: Import jose.jwt, passlib.context.CryptContext
# TODO: Initialize pwd_context with bcrypt scheme


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Return True if plain_password matches the stored hash."""
    # TODO: use pwd_context.verify
    raise NotImplementedError


def get_password_hash(password: str) -> str:
    """Hash a plaintext password with bcrypt."""
    # TODO: use pwd_context.hash
    raise NotImplementedError


def create_access_token(data: dict, expires_delta=None) -> str:
    """Encode a JWT access token with an expiry claim."""
    # TODO: copy data, add exp claim, encode with SECRET_KEY + ALGORITHM
    raise NotImplementedError


def decode_token(token: str):
    """Decode and validate a JWT. Return payload dict or None on failure."""
    # TODO: jwt.decode with try/except JWTError → return None
    raise NotImplementedError
