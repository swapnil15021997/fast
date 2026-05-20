from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ai_model import AIModel


class AIModelRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[AIModel]:
        result = await self._session.execute(select(AIModel).order_by(AIModel.ai_name))
        return list(result.scalars().all())
