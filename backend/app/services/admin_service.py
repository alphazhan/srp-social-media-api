from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException

from app.models.user import User
from app.models.post import Post
from app.schemas.admin import UserStatusUpdate


async def list_all_users(db: AsyncSession):
    """
    Retrieve all registered users (admin-only).
    """
    result = await db.execute(select(User))
    return result.scalars().all()


async def update_user_status(user_id: int, update: UserStatusUpdate, db: AsyncSession):
    """
    Update a user's role and status (admin-only).
    """
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = update.role
    user.status = update.status
    await db.commit()

    return {"message": "User updated"}


async def get_platform_analytics(db: AsyncSession):
    """
    Return total counts of users and posts in the system.
    """
    users = await db.execute(select(User))
    posts = await db.execute(select(Post))

    return {"users": len(users.scalars().all()), "posts": len(posts.scalars().all())}
