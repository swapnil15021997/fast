from fastapi import HTTPException, status

from app.repositories.flow import FlowRepository
from app.schemas.flow import FlowResponse


class FlowService:
    def __init__(self, repo: FlowRepository) -> None:
        self._repo = repo

    async def create(self, flow_name: str, user_id: str) -> FlowResponse:
        flow = await self._repo.create(flow_name, user_id)
        return FlowResponse.model_validate(flow)

    async def get_by_id(self, flow_id: str, user_id: str) -> FlowResponse:
        flow = await self._repo.get_by_id_for_user(flow_id, user_id)
        if not flow:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Flow not found",
            )
        return FlowResponse.model_validate(flow)

    async def list_by_user(self, user_id: str) -> list[FlowResponse]:
        flows = await self._repo.list_by_user(user_id)
        return [FlowResponse.model_validate(f) for f in flows]

    async def update(self, flow_id: str, user_id: str, **kwargs) -> FlowResponse:
        flow = await self._repo.get_by_id_for_user(flow_id, user_id)
        if not flow:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Flow not found",
            )
        cleaned = {k: v for k, v in kwargs.items() if v is not None}
        if not cleaned:
            return FlowResponse.model_validate(flow)
        flow = await self._repo.update(flow, **cleaned)
        return FlowResponse.model_validate(flow)

    async def delete(self, flow_id: str, user_id: str) -> None:
        flow = await self._repo.get_by_id_for_user(flow_id, user_id)
        if not flow:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Flow not found",
            )
        await self._repo.soft_delete(flow)
