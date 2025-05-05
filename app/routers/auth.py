from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from ..database import get_session
from ..models import User, UserCreate
from .. import schema, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login", response_model=schema.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends() , session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == user_credentials.username )).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    # Create a token
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}