"""Security utilities: password hashing and JWT access-token creation."""

import os
from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext


# Configure the hashing algorithm (Argon2id)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plaintext password using Argon2id."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a stored hash."""
    return pwd_context.verify(plain_password, hashed_password)


# SECRET_KEY should be a long, random string set via environment variable in production.
# A hard-coded default is kept here for local development convenience only.
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-for-2026")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


def create_access_token(data: dict) -> str:
    """Create a signed JWT access token that expires in `ACCESS_TOKEN_EXPIRE_MINUTES`."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt