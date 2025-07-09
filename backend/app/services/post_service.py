from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException

from app.models.like import Like
from app.models.post import Post
from app.models.user import User
from app.schemas.post import PostBase, PostCreate, PostExtended, PostUpdate
from app.routers.ws import notify_all
from app.services.ml_service import detect_language, extract_hashtags, moderate_text


async def create_post_for_user(
    post_in: PostCreate, user_id: int, db: AsyncSession
) -> Post:
    """
    Create a new post associated with a given user.
    Includes ML moderation, language detection, and hashtag generation.
    """
    original_text = post_in.content

    # 1. Moderate text
    moderation_result = await moderate_text(original_text)
    if moderation_result["category"] != "OK":
        raise HTTPException(
            status_code=400,
            detail=f"Content rejected: {moderation_result['description']}",
        )

    # 2. Detect language
    language = await detect_language(original_text)

    # 3. Extract hashtags
    hashtags = await extract_hashtags(original_text)
    hashtag_line = " ".join(f"#{tag}" for tag in hashtags)

    # 4. Augment content
    augmented_text = (
        f"{original_text}\n\nDetected language: {language}.\n{hashtag_line}"
    )

    # 5. Create post and update user
    post = Post(content=augmented_text, image_url=post_in.image_url, user_id=user_id)
    db.add(post)

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one()
    user.total_posts += 1

    await db.commit()
    await db.refresh(post)

    await notify_all(f"New post: {post.content}")
    return post


async def list_all_posts(db: AsyncSession):
    """
    Return all posts in the system.
    """
    result = await db.execute(select(Post))
    return result.scalars().all()


async def list_posts_with_user_likes(db: AsyncSession, user_id: int) -> list[dict]:
    result = await db.execute(select(Post).order_by(Post.created_at.desc()))
    posts = result.scalars().all()

    # Fetch all liked post_ids for this user in one go
    liked_ids = await db.execute(select(Like.post_id).where(Like.user_id == user_id))
    liked_set = set(post_id for (post_id,) in liked_ids.all())

    # Attach liked field to each post as a dict
    return [
        PostExtended(
            **PostBase.model_validate(post).model_dump(), liked=(post.id in liked_set)
        )
        for post in posts
    ]


async def update_post_for_user(
    post_id: int, update_data: PostUpdate, user_id: int, db: AsyncSession
) -> Post:
    """
    Update a post if it belongs to the current user.
    Includes content moderation, language detection, and hashtag generation
    when the post content is being changed.
    """
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()

    if not post or post.user_id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized or not found")

    update_fields = update_data.model_dump(exclude_unset=True)

    if "content" in update_fields:
        new_content = update_fields["content"]

        # 1. Moderate text
        moderation_result = await moderate_text(new_content)
        if moderation_result["category"] != "OK":
            raise HTTPException(
                status_code=400,
                detail=f"Content rejected: {moderation_result['description']}",
            )

        # 2. Detect language
        language = await detect_language(new_content)

        # 3. Extract hashtags
        hashtags = await extract_hashtags(new_content)
        hashtag_line = " ".join(f"#{tag}" for tag in hashtags)

        # 4. Augment content
        update_fields["content"] = (
            f"{new_content}\n\nDetected language: {language}\n{hashtag_line}"
        )

    for key, value in update_fields.items():
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

    # Decrement total_posts count before deleting
    user_result = await db.execute(select(User).where(User.id == user_id))
    user = user_result.scalar_one_or_none()
    if user and user.total_posts > 0:
        user.total_posts -= 1

    await db.delete(post)
    await db.commit()


async def get_post_by_id(post_id: int, db: AsyncSession) -> Post:
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


async def get_posts_by_user_id(user_id: int, db: AsyncSession) -> list[Post]:
    result = await db.execute(select(Post).where(Post.user_id == user_id))
    return result.scalars().all()
