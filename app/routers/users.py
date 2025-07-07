from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.models.user import User
from app.schemas import user as user_schema
from app.utils.security import get_current_user
from app.services.user_service import get_user_by_id

router = APIRouter()


@router.get("/me", response_model=user_schema.UserBase)
async def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/{user_id}", response_model=user_schema.UserBase)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await get_user_by_id(user_id, db)
