# app/routers/comments.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.models.user import User
from app.schemas import comment as comment_schema
from app.schemas import like as like_schema
from app.utils.security import get_current_user
from app.services.comment_service import (
    create_comment,
    get_comments_for_post,
    update_comment,
    delete_comment,
)

router = APIRouter()


@router.post("/posts/{post_id}/comments", response_model=comment_schema.CommentBase)
async def add_comment(
    post_id: int,
    comment_in: comment_schema.CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await create_comment(post_id, current_user.id, comment_in, db)


@router.get(
    "/posts/{post_id}/comments", response_model=list[comment_schema.CommentBase]
)
async def get_comments(post_id: int, db: AsyncSession = Depends(get_db)):
    return await get_comments_for_post(post_id, db)


@router.put("/comments/{comment_id}", response_model=comment_schema.CommentBase)
async def edit_comment(
    comment_id: int,
    update: comment_schema.CommentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await update_comment(comment_id, current_user.id, update, db)


@router.delete("/comments/{comment_id}", status_code=204)
async def remove_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await delete_comment(comment_id, current_user.id, db)
