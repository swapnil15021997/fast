from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.refresh_token import RefreshToken
from app.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, email: str, hashed_password: str, name: str) -> User:
        user = User(
            id=str(uuid4()),
            email=email,
            hashed_password=hashed_password,
            name=name,
        )
        self._session.add(user)
        await self._session.flush()
        return user

    async def get_by_email(self, email: str) -> User | None:
        result = await self._session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: str) -> User | None:
        return await self._session.get(User, user_id)

    async def save_refresh_token(self, user_id: str, token: str) -> RefreshToken:
        rt = RefreshToken(
            id=str(uuid4()),
            user_id=user_id,
            token=token,
        )
        self._session.add(rt)
        await self._session.flush()
        return rt

    async def get_refresh_token(self, token: str) -> RefreshToken | None:
        result = await self._session.execute(
            select(RefreshToken).where(
                RefreshToken.token == token,
                RefreshToken.is_revoked == False,
            )
        )
        return result.scalar_one_or_none()

    async def revoke_refresh_token(self, token: RefreshToken) -> None:
        token.is_revoked = True
        await self._session.flush()
