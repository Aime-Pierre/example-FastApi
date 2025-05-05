from ..database import engine, get_session
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlmodel import Session
from ..models import Post, User, UserCreate, Vote
from sqlmodel import select
from .. import schema, oauth2
from typing import Optional

router = APIRouter(
    prefix="/votes",
    tags=["votes",]
    
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(vote: schema.Vote, session: Session = Depends(get_session), user_id: int = Depends(oauth2.get_current_user)):

    vote_query = session.exec(select(Vote).where(Vote.post_id == vote.post_id, Vote.user_id == user_id.id))
    found_vote = vote_query.first()   

    #If post does not exist, raise an error
    post = session.exec(select(Post).where(Post.id == vote.post_id)).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} does not exist")
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {user_id.id} has already voted on post {vote.post_id}")
        new_vote = Vote(post_id=vote.post_id, user_id=user_id.id)
        session.add(new_vote)   
        session.commit()
        return {"message": "Vote added successfully"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote not found")
        session.delete(found_vote)
        session.commit()
        return {"message": "Vote deleted successfully"} 
