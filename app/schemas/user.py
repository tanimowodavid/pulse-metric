"""Pydantic schemas for user-related API payloads."""

from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """Incoming payload for user registration."""

    email: EmailStr
    company_name: str
    password: str


class UserOut(BaseModel):
    """Shape of user data returned to API consumers."""

    id: str
    email: EmailStr
    company_name: str
    created_at: datetime

    class Config:
        # Tells Pydantic to read data from SQLAlchemy objects via attribute access.
        from_attribute = True