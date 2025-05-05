from ..database import engine, get_session
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlmodel import Session
from ..models import Post, User, UserCreate, Vote
from sqlmodel import select
from sqlalchemy.sql import func
from sqlalchemy.orm import joinedload
from .. import schema, oauth2
from typing import Optional

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
    
)

@router.get("/", response_model=list[schema.PostOUT])
def get_posts(session: Session = Depends(get_session), user_id: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, 
              search: Optional[str] = ""):  
    post = session.exec(
        select(Post, func.count(Vote.post_id).label("vote_count"))
        .join(Vote, Vote.post_id == Post.id, isouter=True)
        .group_by(Post.id)
        .where(Post.title.contains(search))
        .offset(skip)
        .limit(limit)
    ).all()

    return schema.serialize_posts_with_votes(post)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.PostResponse)
def create_posts(post: Post, session: Session = Depends(get_session), user_id: int = Depends(oauth2.get_current_user)):
    post = Post(owner_id=user_id.id, **post.model_dump())
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

@router.get("/{id}", response_model=schema.PostOUT)
def get_post(id: int, session: Session = Depends(get_session), user_id: int = Depends(oauth2.get_current_user)):
    result = session.exec(
        select(Post, func.count(Vote.post_id).label("vote_count"))
        .join(Vote, Vote.post_id == Post.id, isouter=True)
        .group_by(Post.id).where(Post.id == id)
    ).first()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")

    post, vote_count = result  # Unpack the tuple

    # Pass the unpacked post and vote_count to the serializer
    return schema.serialize_posts_with_votes([(post, vote_count)])[0]

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)  
def delete_post(id: int, sesion: Session = Depends(get_session), user_id: int = Depends(oauth2.get_current_user)):
    post = sesion.get(Post, id)

    if not post:    
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    if  post.owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    if post and post.owner_id == user_id.id:
        sesion.delete(post)
        sesion.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schema.PostResponse)    
def update_post(id: int, post_data: Post, session: Session = Depends(get_session), user_id: int = Depends(oauth2.get_current_user)):
    post = session.get(Post, id)
    if not post:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    if post.owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    if post and post.owner_id == user_id.id:
        # Update the post with the new data
        post_to_update = post_data.model_dump(exclude_unset=True)
        for key, value in post_to_update.items():
            setattr(post, key, value)
        session.commit()
        session.refresh(post)
        return post

