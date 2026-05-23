from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_ai_token import UserAIToken


class UserAITokenRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_or_create(self, user_id: str, period_start: str, period_end: str) -> UserAIToken:
        result = await self._session.execute(
            select(UserAIToken).where(
                UserAIToken.user_id == user_id,
                UserAIToken.period_start == period_start,
                UserAIToken.period_end == period_end,
            )
        )
        token = result.scalar_one_or_none()
        if token:
            return token
        token = UserAIToken(
            id=str(uuid4()),
            user_id=user_id,
            period_start=period_start,
            period_end=period_end,
        )
        self._session.add(token)
        await self._session.flush()
        return token

    async def get_by_user_id(self, user_id: str) -> list[UserAIToken]:
        result = await self._session.execute(
            select(UserAIToken).where(UserAIToken.user_id == user_id)
        )
        return list(result.scalars().all())

    async def add_tokens(self, token: UserAIToken, amount: int) -> UserAIToken:
        token.tokens_used = UserAIToken.tokens_used + amount
        await self._session.flush()
        return token

    async def update(self, token: UserAIToken, **kwargs) -> UserAIToken:
        for key, value in kwargs.items():
            setattr(token, key, value)
        await self._session.flush()
        return token
