from fastapi import APIRouter, Depends

from app.core.dependencies import (
    get_ai_model_repository,
    get_current_user_id,
    get_user_repository,
)
from app.repositories.ai_model import AIModelRepository
from app.repositories.user import UserRepository
from app.schemas.ai_model import AIModelCreate, AIModelResponse, AIModelUpdate

router = APIRouter()


@router.get("", response_model=list[AIModelResponse])
async def list_ai_models(
    repo: AIModelRepository = Depends(get_ai_model_repository),
) -> list[AIModelResponse]:
    models = await repo.list_all()
    return [AIModelResponse.model_validate(m) for m in models]


@router.post("", response_model=AIModelResponse, status_code=201)
async def create_ai_model(
    body: AIModelCreate,
    user_id: int = Depends(get_current_user_id),
    user_repo: UserRepository = Depends(get_user_repository),
    repo: AIModelRepository = Depends(get_ai_model_repository),
) -> AIModelResponse:
    user = await user_repo.get_by_id(user_id)
    if not user or not user.is_superuser:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only superusers can create AI models",
        )
    model = await repo.create(ai_name=body.ai_name)
    return AIModelResponse.model_validate(model)


@router.patch("/{ai_id}", response_model=AIModelResponse)
async def update_ai_model(
    ai_id: int,
    body: AIModelUpdate,
    user_id: int = Depends(get_current_user_id),
    user_repo: UserRepository = Depends(get_user_repository),
    repo: AIModelRepository = Depends(get_ai_model_repository),
) -> AIModelResponse:
    from fastapi import HTTPException, status
    user = await user_repo.get_by_id(user_id)
    if not user or not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only superusers can update AI models",
        )
    model = await repo.get_by_id(ai_id)
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AI model not found",
        )
    cleaned = {k: v for k, v in body.model_dump().items() if v is not None}
    if cleaned:
        model = await repo.update(model, **cleaned)
    return AIModelResponse.model_validate(model)


@router.delete("/{ai_id}", status_code=204)
async def delete_ai_model(
    ai_id: int,
    user_id: int = Depends(get_current_user_id),
    user_repo: UserRepository = Depends(get_user_repository),
    repo: AIModelRepository = Depends(get_ai_model_repository),
) -> None:
    from fastapi import HTTPException, status
    user = await user_repo.get_by_id(user_id)
    if not user or not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only superusers can delete AI models",
        )
    model = await repo.get_by_id(ai_id)
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AI model not found",
        )
    await repo.delete(model)
