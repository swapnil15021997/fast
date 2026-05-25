from uuid import uuid4

from fastapi import HTTPException, status

from app.core.config import settings
from app.repositories.flow import FlowRepository
from app.schemas.flow import FlowResponse, FlowPublicResponse
from app.schemas.public import PublicShareResponse


class PublicService:
    def __init__(self, repo: FlowRepository) -> None:
        self._repo = repo

    async def enable_sharing(self, flow_id: int, user_id: int) -> PublicShareResponse:
        flow = await self._repo.get_by_id_for_user(flow_id, user_id)
        if not flow:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Flow not found",
            )
        if flow.public_token:
            token = flow.public_token
        else:
            token = str(uuid4())
            await self._repo.update(flow, is_public=True, public_token=token)
        share_url = f"{settings.public_base_url}/{token}"
        return PublicShareResponse(public_token=token, share_url=share_url)

    async def disable_sharing(self, flow_id: int, user_id: int) -> FlowResponse:
        flow = await self._repo.get_by_id_for_user(flow_id, user_id)
        if not flow:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Flow not found",
            )
        await self._repo.update(flow, is_public=False, public_token=None)
        return FlowResponse.model_validate(flow)

    async def get_public_flow(self, public_token: str) -> FlowPublicResponse:
        flow = await self._repo.get_by_public_token(public_token)
        if not flow:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shared flow not found or no longer public",
            )
        return FlowPublicResponse.model_validate(flow)
