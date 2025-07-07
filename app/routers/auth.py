from fastapi import APIRouter, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.schemas import auth as auth_schema, user as user_schema
from app.services.auth_service import register_user, login_user

router = APIRouter()


@router.post("/register", response_model=user_schema.UserBase)
async def register_user_handler(
    user_in: user_schema.UserCreate, db: AsyncSession = Depends(get_db)
):
    return await register_user(user_in, db)


@router.post("/login", response_model=auth_schema.Token)
async def login_user_handler(
    username: str = Form(
        ...
    ),  # Swagger always calls it "username", but we can also accept "email."
    password: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    credentials = auth_schema.LoginRequest(
        username_or_email=username, password=password
    )
    return await login_user(credentials, db)
