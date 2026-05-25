from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ai_model import AIModel


class AIModelRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[AIModel]:
        result = await self._session.execute(select(AIModel).order_by(AIModel.ai_name))
        return list(result.scalars().all())

    async def create(self, ai_name: str) -> AIModel:
        model = AIModel(ai_name=ai_name)
        self._session.add(model)
        await self._session.flush()
        return model

    async def get_by_id(self, ai_id: int) -> AIModel | None:
        return await self._session.get(AIModel, ai_id)

    async def update(self, model: AIModel, **kwargs) -> AIModel:
        for key, value in kwargs.items():
            setattr(model, key, value)
        await self._session.flush()
        return model

    async def delete(self, model: AIModel) -> None:
        await self._session.delete(model)
        await self._session.flush()
