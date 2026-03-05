from passlib.context import CryptContext
from sqlalchemy.util import deprecated
from datetime import datetime, timedelta, timezone
from jose import jwt


# Define the hashing algorithm (Argon2id)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)



# SECRET_KEY should be a long, random string in your .env file
SECRET_KEY = "your-super-secret-key-for-2026" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    """Creates a signed JWT token that expires in 1 hour."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # This signs the data with your secret key
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt