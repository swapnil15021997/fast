from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user_id, get_public_service, get_flow_service
from app.schemas.flow import FlowPublicResponse, FlowResponse
from app.schemas.public import PublicShareResponse
from app.services.public import PublicService
from app.services.flow import FlowService

router = APIRouter()


@router.post("/flows/{flow_id}/share", response_model=PublicShareResponse)
async def enable_sharing(
    flow_id: int,
    user_id: int = Depends(get_current_user_id),
    public_service: PublicService = Depends(get_public_service),
) -> PublicShareResponse:
    return await public_service.enable_sharing(flow_id, user_id)


@router.delete("/flows/{flow_id}/share", response_model=FlowResponse)
async def disable_sharing(
    flow_id: int,
    user_id: int = Depends(get_current_user_id),
    public_service: PublicService = Depends(get_public_service),
) -> FlowResponse:
    return await public_service.disable_sharing(flow_id, user_id)


@router.get("/share/{public_token}", response_model=FlowPublicResponse)
async def get_public_flow(
    public_token: str,
    public_service: PublicService = Depends(get_public_service),
) -> FlowPublicResponse:
    return await public_service.get_public_flow(public_token)
