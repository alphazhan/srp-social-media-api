from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.models.user import User
from app.schemas import like as like_schema
from app.utils.security import get_current_user
from app.services.like_service import (
    get_likes_for_post,
    like_post_by_user,
    unlike_post_by_user,
    has_user_liked_post,
)

router = APIRouter()


@router.post("/posts/{post_id}/like", response_model=like_schema.LikeBase)
async def like_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await like_post_by_user(post_id, current_user.id, db)


@router.delete("/posts/{post_id}/like", status_code=204)
async def unlike_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await unlike_post_by_user(post_id, current_user.id, db)


@router.get("/posts/{post_id}/likes", response_model=list[like_schema.LikeBase])
async def get_likes(post_id: int, db: AsyncSession = Depends(get_db)):
    return await get_likes_for_post(post_id, db)


@router.get("/posts/{post_id}/like-status", response_model=bool)
async def check_if_user_liked_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await has_user_liked_post(post_id, current_user.id, db)
