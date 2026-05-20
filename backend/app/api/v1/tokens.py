from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user_id, get_token_service
from app.schemas.token import TokenUsageResponse
from app.services.token import TokenService

router = APIRouter()


@router.get("/usage", response_model=TokenUsageResponse)
async def get_token_usage(
    user_id: str = Depends(get_current_user_id),
    token_service: TokenService = Depends(get_token_service),
) -> TokenUsageResponse:
    return await token_service.get_usage(user_id)
