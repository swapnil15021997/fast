from uuid import uuid4

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.flow import Flow


class FlowRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, flow_name: str, user_id: str) -> Flow:
        flow = Flow(
            flow_id=str(uuid4()),
            flow_name=flow_name,
            flow_user_id=user_id,
        )
        self._session.add(flow)
        await self._session.flush()
        return flow

    async def get_by_id(self, flow_id: str) -> Flow | None:
        return await self._session.get(Flow, flow_id)

    async def get_by_id_for_user(self, flow_id: str, user_id: str) -> Flow | None:
        result = await self._session.execute(
            select(Flow).where(
                Flow.flow_id == flow_id,
                Flow.flow_user_id == user_id,
                Flow.flow_is_delete == False,
            )
        )
        return result.scalar_one_or_none()

    async def list_by_user(self, user_id: str) -> list[Flow]:
        result = await self._session.execute(
            select(Flow)
            .where(Flow.flow_user_id == user_id, Flow.flow_is_delete == False)
            .order_by(Flow.created_at.desc())
        )
        return list(result.scalars().all())

    async def update(self, flow: Flow, **kwargs) -> Flow:
        for key, value in kwargs.items():
            setattr(flow, key, value)
        await self._session.flush()
        return flow

    async def soft_delete(self, flow: Flow) -> None:
        flow.flow_is_delete = True
        await self._session.flush()

    async def get_by_public_token(self, public_token: str) -> Flow | None:
        result = await self._session.execute(
            select(Flow).where(
                Flow.public_token == public_token,
                Flow.is_public == True,
                Flow.flow_is_delete == False,
            )
        )
        return result.scalar_one_or_none()
