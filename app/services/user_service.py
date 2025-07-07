# User retrieval and updates

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.models.user import User
from app.schemas.user import UserUpdate


async def get_user_by_id(user_id: int, db: AsyncSession) -> User:
    """
    Fetch a user by their ID or raise 404 if not found.
    """
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def update_user_profile(
    user: User, update_data: UserUpdate, db: AsyncSession
) -> User:
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    await db.commit()
    await db.refresh(user)
    return user
