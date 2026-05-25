from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user_id, get_flow_service
from app.schemas.flow import FlowCreate, FlowResponse, FlowUpdate
from app.services.flow import FlowService

router = APIRouter()


@router.post("", response_model=FlowResponse, status_code=201)
async def create_flow(
    body: FlowCreate,
    user_id: int = Depends(get_current_user_id),
    flow_service: FlowService = Depends(get_flow_service),
) -> FlowResponse:
    return await flow_service.create(flow_name=body.flow_name, user_id=user_id)


@router.get("", response_model=list[FlowResponse])
async def list_flows(
    user_id: int = Depends(get_current_user_id),
    flow_service: FlowService = Depends(get_flow_service),
) -> list[FlowResponse]:
    return await flow_service.list_by_user(user_id)


@router.get("/{flow_id}", response_model=FlowResponse)
async def get_flow(
    flow_id: int,
    user_id: int = Depends(get_current_user_id),
    flow_service: FlowService = Depends(get_flow_service),
) -> FlowResponse:
    return await flow_service.get_by_id(flow_id, user_id)


@router.patch("/{flow_id}", response_model=FlowResponse)
async def update_flow(
    flow_id: int,
    body: FlowUpdate,
    user_id: int = Depends(get_current_user_id),
    flow_service: FlowService = Depends(get_flow_service),
) -> FlowResponse:
    return await flow_service.update(
        flow_id, user_id,
        flow_name=body.flow_name,
        flow_json=body.flow_json,
        flow_connection_json=body.flow_connection_json,
    )


@router.delete("/{flow_id}", status_code=204)
async def delete_flow(
    flow_id: int,
    user_id: int = Depends(get_current_user_id),
    flow_service: FlowService = Depends(get_flow_service),
) -> None:
    await flow_service.delete(flow_id, user_id)
