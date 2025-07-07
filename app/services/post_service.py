from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException

from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate


async def create_post_for_user(
    post_in: PostCreate, user_id: int, db: AsyncSession
) -> Post:
    """
    Create a new post associated with a given user.
    """
    post = Post(**post_in.model_dump(), user_id=user_id)
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post


async def list_all_posts(db: AsyncSession):
    """
    Return all posts in the system.
    """
    result = await db.execute(select(Post))
    return result.scalars().all()


async def update_post_for_user(
    post_id: int, update_data: PostUpdate, user_id: int, db: AsyncSession
) -> Post:
    """
    Update a post if it belongs to the current user.
    """
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()

    if not post or post.user_id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized or not found")

    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(post, key, value)

    await db.commit()
    await db.refresh(post)
    return post


async def delete_post_for_user(post_id: int, user_id: int, db: AsyncSession):
    """
    Delete a post if it belongs to the current user.
    """
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()

    if not post or post.user_id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized or not found")

    await db.delete(post)
    await db.commit()
