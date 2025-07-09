from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException

from app.models.comment import Comment
from app.models.post import Post
from app.schemas.comment import CommentCreate, CommentUpdate
from app.services.ml_service import detect_language, moderate_text


async def create_comment(
    post_id: int, user_id: int, data: CommentCreate, db: AsyncSession
) -> Comment:
    """
    Create a comment for the given post, with moderation and language metadata.
    """
    # Ensure the post exists before commenting
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # 1. Moderate comment text
    moderation = await moderate_text(data.text)
    if moderation["category"] != "OK":
        raise HTTPException(
            status_code=400, detail=f"Comment rejected: {moderation['description']}"
        )

    # 2. Detect language
    lang = await detect_language(data.text)
    augmented_text = f"{data.text}\n\nDetected language: {lang}"

    # 3. Create and persist comment
    comment = Comment(text=augmented_text, post_id=post_id, user_id=user_id)
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment


async def get_comments_for_post(post_id: int, db: AsyncSession):
    """
    Fetch all comments for a given post ID.
    """
    result = await db.execute(select(Comment).where(Comment.post_id == post_id))
    return result.scalars().all()


async def update_comment(
    comment_id: int, user_id: int, update: CommentUpdate, db: AsyncSession
) -> Comment:
    """
    Update a comment's text with moderation and language enrichment.
    """
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    comment = result.scalar_one_or_none()

    if not comment or comment.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed to edit this comment")

    # 1. Moderate
    moderation = await moderate_text(update.text)
    if moderation["category"] != "OK":
        raise HTTPException(
            status_code=400, detail=f"Comment rejected: {moderation['description']}"
        )

    # 2. Language detection
    lang = await detect_language(update.text)
    comment.text = f"{update.text}\n\nDetected language: {lang}"

    await db.commit()
    await db.refresh(comment)
    return comment


async def delete_comment(comment_id: int, user_id: int, db: AsyncSession):
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    comment = result.scalar_one_or_none()
    if not comment or comment.user_id != user_id:
        raise HTTPException(
            status_code=403, detail="Not allowed to delete this comment"
        )

    await db.delete(comment)
    await db.commit()
