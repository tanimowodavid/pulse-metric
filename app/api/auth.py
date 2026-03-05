from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
import uuid

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserOut, status_code=201)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # create the user object
    new_user = User(
        id=str(uuid.uuid4()),
        email=user_data.email,
        company_name=user_data.company_name,
       password_hash=hash_password(user_data.password)
    )

    # save to DB
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



@router.post("/token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    # OAuth2 form uses 'username' field for the email
    user = db.query(User).filter(User.email == form_data.username).first()
    
    # Verify existence and password
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate the token
    access_token = create_access_token(data={"sub": user.email})
    
    # Return in the standard OAuth2 format
    return {"access_token": access_token, "token_type": "bearer"}