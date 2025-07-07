# Custom validation logic (e.g., email uniqueness, password strength)

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User


async def validate_unique_email(email: str, db: AsyncSession):
    result = await db.execute(select(User).where(User.email == email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")


# For example, `await validate_unique_email(user_in.email, db)`
