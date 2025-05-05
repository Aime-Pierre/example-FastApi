from ..database import engine, get_session
from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session
from ..models import User, UserCreate
from .. import schema, utils

router = APIRouter(
    prefix="/users",
    tags=["Users"]

)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserResponse)
def create_user(user_data: UserCreate, session: Session = Depends(get_session)):

    #Hash the password
    hashed_password = utils.hash_password(user_data.password)
    user_data.password = hashed_password

    user_db = User(**user_data.model_dump())
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db

@router.get("/{id}", response_model=schema.UserResponse)
def get_user(id: int, session: Session = Depends(get_session)):
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} was not found")
    return user