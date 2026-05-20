from fastapi import APIRouter, Depends

from app.core.dependencies import get_ai_model_repository
from app.repositories.ai_model import AIModelRepository
from app.schemas.ai_model import AIModelResponse

router = APIRouter()


@router.get("", response_model=list[AIModelResponse])
async def list_ai_models(
    repo: AIModelRepository = Depends(get_ai_model_repository),
) -> list[AIModelResponse]:
    models = await repo.list_all()
    return [AIModelResponse.model_validate(m) for m in models]
