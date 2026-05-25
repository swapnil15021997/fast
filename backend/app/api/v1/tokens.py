from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user_id, get_token_repository, get_token_service
from app.schemas.token import TokenUpdate, TokenUsageResponse, UserAITokenResponse
from app.services.token import TokenService

router = APIRouter()


@router.get("/usage", response_model=TokenUsageResponse)
async def get_token_usage(
    user_id: int = Depends(get_current_user_id),
    token_service: TokenService = Depends(get_token_service),
) -> TokenUsageResponse:
    return await token_service.get_usage(user_id)


@router.get("", response_model=list[UserAITokenResponse])
async def list_token_settings(
    user_id: int = Depends(get_current_user_id),
    token_repo=Depends(get_token_repository),
) -> list[UserAITokenResponse]:
    tokens = await token_repo.get_by_user_id(user_id)
    return [UserAITokenResponse.model_validate(t) for t in tokens]


@router.patch("", response_model=UserAITokenResponse)
async def update_token_settings(
    body: TokenUpdate,
    user_id: int = Depends(get_current_user_id),
    token_repo=Depends(get_token_repository),
) -> UserAITokenResponse:
    from datetime import datetime, timedelta

    today = datetime.utcnow().strftime("%Y-%m-%d")
    period_end = (datetime.utcnow() + timedelta(days=30)).strftime("%Y-%m-%d")
    tokens = await token_repo.get_by_user_id(user_id)
    token = tokens[0] if tokens else await token_repo.get_or_create(user_id, today, period_end)
    updates = {}
    if body.ai_model_id is not None:
        updates["ai_model_id"] = body.ai_model_id
    if body.tokens_limit is not None:
        updates["tokens_limit"] = body.tokens_limit
    if body.ai_token is not None:
        updates["ai_token"] = body.ai_token
    if updates:
        token = await token_repo.update(token, **updates)
    return UserAITokenResponse.model_validate(token)
