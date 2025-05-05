from  sqlmodel import SQLModel, Field, Relationship, text
from pydantic import EmailStr, field_validator
from typing import Optional


# Schéma de validation (hérite de UserBase)
class UserCreate(SQLModel):
    email: EmailStr  # ✅ Validation Pydantic (surcharge du champ)
    password: str 

# Modèle de base de données (hérite de UserBase)
class User(UserCreate, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, nullable=False)  # Configuration DB
    password: str
    created_at: str | None = Field(
        default=None, 
        sa_column_kwargs={"server_default": text("now()")}
    )
    posts: list["Post"] = Relationship(back_populates="user")
    votes: list["Vote"] = Relationship(back_populates="user")   

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    title: str
    content: str 
    published: bool = Field(
        default=True, 
        sa_column_kwargs={"server_default": text("TRUE")}
    )
    created_at: Optional[str] = Field(
        default=None, 
        sa_column_kwargs={"server_default": text("now()")}
    )
    owner_id: int = Field(
        foreign_key="user.id", 
        ondelete="CASCADE",
        nullable=False
    )
    user: User | None = Relationship(back_populates="posts")
    votes: list["Vote"] = Relationship(back_populates="post")


class Vote(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id", ondelete="CASCADE" , primary_key=True)
    post_id: int = Field(foreign_key="post.id", ondelete="CASCADE", primary_key=True)
    post: Post | None = Relationship(back_populates="votes")
    user: User | None = Relationship(back_populates="votes")
