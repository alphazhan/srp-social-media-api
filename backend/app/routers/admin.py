from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.models.user import User
from app.schemas.admin import UserStatusUpdate
from app.utils.dependencies import require_admin
from app.services.admin_service import (
    list_all_users,
    update_user_status,
    get_platform_analytics,
)

router = APIRouter()


@router.get("/users")
async def list_users(
    db: AsyncSession = Depends(get_db), _: User = Depends(require_admin)
):
    return await list_all_users(db)


@router.put("/users/{user_id}/status")
async def update_user(
    user_id: int,
    update: UserStatusUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_admin),
):
    return await update_user_status(user_id, update, db)


@router.get("/analytics")
async def analytics(
    db: AsyncSession = Depends(get_db), _: User = Depends(require_admin)
):
    return await get_platform_analytics(db)
