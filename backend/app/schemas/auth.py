from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class LoginRequest(BaseModel):
    username_or_email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    sub: Optional[str] = None


class AuthUserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: str
    created_at: datetime

    class Config:
        orm_mode = True
