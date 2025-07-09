from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.models.user import User
from app.schemas import user as user_schema
from app.schemas import post as post_schema
from app.utils.security import get_current_user
from app.services.user_service import (
    get_user_by_id,
    create_user,
    update_user_profile,
    delete_user,
    get_posts_by_user,
)

router = APIRouter()


@router.get("/me", response_model=user_schema.UserBase)
async def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/{user_id}", response_model=user_schema.UserBase)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await get_user_by_id(user_id, db)


@router.post("", response_model=user_schema.UserBase)
async def register_user_direct(
    user_in: user_schema.UserCreate, db: AsyncSession = Depends(get_db)
):
    return await create_user(user_in, db)


@router.put("/{user_id}", response_model=user_schema.UserBase)
async def update_profile(
    user_id: int, update: user_schema.UserUpdate, db: AsyncSession = Depends(get_db)
):
    return await update_user_profile(user_id, update, db)


@router.delete("/{user_id}", status_code=204)
async def delete_profile(user_id: int, db: AsyncSession = Depends(get_db)):
    await delete_user(user_id, db)


@router.get("/{user_id}/posts", response_model=list[post_schema.PostBase])
async def get_user_posts(user_id: int, db: AsyncSession = Depends(get_db)):
    return await get_posts_by_user(user_id, db)
