from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from datetime import timedelta

from app.models.user import User
from app.schemas.auth import LoginRequest
from app.schemas.user import UserCreate
from app.utils.security import get_password_hash, verify_password, create_access_token


async def register_user(user_in: UserCreate, db: AsyncSession) -> User:
    """
    Create a new user with hashed password, ensuring unique email.
    """
    result = await db.execute(select(User).where(User.email == user_in.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_pw = get_password_hash(user_in.password)
    user = User(**user_in.model_dump(exclude={"password"}), hashed_password=hashed_pw)

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def login_user(credentials: LoginRequest, db: AsyncSession) -> dict:
    """
    Authenticate a user and return a JWT token on success.
    """
    identifier = credentials.username_or_email

    stmt = select(User).where(
        (User.email == identifier) | (User.username == identifier)
    )
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=timedelta(minutes=60)
    )
    return {"access_token": token, "token_type": "bearer"}
