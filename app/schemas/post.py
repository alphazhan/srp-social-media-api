from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schema used when creating a post (request body)


class PostCreate(BaseModel):
    content: str  # Required text content
    image_url: Optional[str] = None  # Optional image URL


# Schema used when updating a post (PATCH/PUT)


class PostUpdate(BaseModel):
    content: Optional[str] = None  # Optional text change
    image_url: Optional[str] = None  # Optional image change


# Schema used when returning a post (GET response)


class PostBase(BaseModel):
    id: int
    content: str
    image_url: Optional[str]
    user_id: int  # ID of the author
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True  # Enables compatibility with SQLAlchemy models
