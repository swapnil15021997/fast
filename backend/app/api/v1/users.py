from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user_id, get_user_service
from app.schemas.user import UserResponse
from app.services.user import UserService

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_me(
    user_id: str = Depends(get_current_user_id),
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    return await user_service.get_by_id(user_id)
