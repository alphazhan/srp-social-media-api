from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.models.user import User
from app.schemas import post as post_schema
from app.utils.security import get_current_user
from app.services.post_service import (
    create_post_for_user,
    list_all_posts,
    update_post_for_user,
    delete_post_for_user,
    get_post_by_id,
    get_posts_by_user_id,
)

router = APIRouter()


@router.post("/", response_model=post_schema.PostBase)
async def create_post(
    post_in: post_schema.PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await create_post_for_user(post_in, current_user.id, db)


@router.get("/", response_model=list[post_schema.PostBase])
async def get_posts(db: AsyncSession = Depends(get_db)):
    return await list_all_posts(db)


@router.put("/{post_id}", response_model=post_schema.PostBase)
async def update_post(
    post_id: int,
    post_in: post_schema.PostUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await update_post_for_user(post_id, post_in, current_user.id, db)


@router.delete("/{post_id}", status_code=204)
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await delete_post_for_user(post_id, current_user.id, db)


@router.get("/{post_id}", response_model=post_schema.PostBase)
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    return await get_post_by_id(post_id, db)


@router.get("/user/{user_id}", response_model=list[post_schema.PostBase])
async def get_posts_by_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await get_posts_by_user_id(user_id, db)
