from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime

class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime
    @field_validator('created_at')
    def format_datetime(cls, v: datetime) -> str:
        return v.isoformat()
    

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True
    owner_id: int
    user: Optional[UserResponse] = None

class PostOUT(BaseModel):
    Post: PostResponse
    Vote: int

# Updated serialization function to align with the schema

def serialize_posts_with_votes(post):
    return [
        PostOUT(
            Post=PostResponse(
                id=post.id,
                title=post.title,
                content=post.content,
                published=post.published,
                owner_id=post.owner_id,
                user=UserResponse(
                    id=post.user.id,
                    email=post.user.email,
                    created_at=post.user.created_at
                ) if post.user else None
            ),
            Vote=votes
        ) for post, votes in post
    ]

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int | None = None

class Vote(BaseModel):
    post_id: int
    dir: int = Field(..., le=1)
