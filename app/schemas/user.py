from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum

# Enums to mirror the Role and Status from the SQL model (used in response serialization)


class Role(str, Enum):
    user = "user"
    moderator = "moderator"
    admin = "admin"


class Status(str, Enum):
    active = "active"
    banned = "banned"


# Schema used when creating a new user (input payload)


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)  # Must be 3-50 chars
    email: EmailStr  # Valid email format required
    full_name: str  # Required full name
    password: str = Field(
        ..., min_length=6
    )  # Raw password input (to be hashed by backend)


# Schema used when updating a user's profile (input)


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    profile_image_url: Optional[str] = None


# Schema used when sending user info back to the client (response)


class UserBase(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: str
    bio: Optional[str]
    profile_image_url: Optional[str]
    total_posts: int
    created_at: datetime
    last_active: Optional[datetime]  # Could be null if never logged in
    role: Role
    status: Status

    class Config:
        orm_mode = (
            True  # Allows SQLAlchemy ORM instances to be serialized automatically
        )
