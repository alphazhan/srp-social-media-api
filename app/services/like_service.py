from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException

from app.models.like import Like
from app.models.post import Post


async def like_post_by_user(post_id: int, user_id: int, db: AsyncSession) -> Like:
    """
    Like a post on behalf of the user.
    """
    # Ensure the post exists
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Check if already liked (optional safety)
    existing_like = await db.execute(
        select(Like).where(Like.user_id == user_id, Like.post_id == post_id)
    )
    if existing_like.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Post already liked")

    # Create new Like entry
    like = Like(user_id=user_id, post_id=post_id)
    db.add(like)
    await db.commit()
    await db.refresh(like)
    return like


async def unlike_post_by_user(post_id: int, user_id: int, db: AsyncSession):
    """
    Unlike a post if the like exists.
    """
    result = await db.execute(
        select(Like).where(Like.user_id == user_id, Like.post_id == post_id)
    )
    like = result.scalar_one_or_none()
    if not like:
        raise HTTPException(status_code=404, detail="Like not found")

    await db.delete(like)
    await db.commit()
