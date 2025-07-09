from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Input schema for creating a new comment


class CommentCreate(BaseModel):
    text: str  # Required comment text


# Input schema for updating an existing comment (partial allowed)


class CommentUpdate(BaseModel):
    text: Optional[str] = None  # Optional: only update if provided


# Output schema for returning comment data to the client


class CommentBase(BaseModel):
    id: int
    text: str
    user_id: int
    post_id: int
    created_at: datetime
    updated_at: Optional[datetime]  # May be null if never updated

    class Config:
        orm_mode = True  # Enables response from SQLAlchemy ORM objects
