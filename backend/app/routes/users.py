from fastapi import APIRouter, Depends

from app.auth import current_active_user
from app.models.user import User
from app.schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
async def get_me(user: User = Depends(current_active_user)):
    return user
