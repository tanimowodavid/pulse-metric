from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID

# Registration Data
class UserCreate(BaseModel):
    email: EmailStr
    company_name: str
    password: str

# user info
class UserOut(BaseModel):
    id: str
    email: EmailStr
    company_name: str
    created_at: datetime

    class Config:
        from_attribute = True  # Tells Pydantic to read data from SQLAlchemy objects