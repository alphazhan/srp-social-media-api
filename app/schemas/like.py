from pydantic import BaseModel
from datetime import datetime

# Response schema for a like record


class LikeBase(BaseModel):
    id: int  # Like ID (if you want to expose it)
    user_id: int  # ID of the user who liked the post
    post_id: int  # ID of the post that was liked
    created_at: datetime  # Time when the like was added

    class Config:
        orm_mode = True  # Allows SQLAlchemy objects to be returned directly
