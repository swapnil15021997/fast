from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token
from app.db.session import get_session
from app.repositories.user import UserRepository
from app.services.auth import AuthService
from app.services.user import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_session_dependency() -> AsyncSession:
    async for session in get_session():
        yield session


def get_user_repository(
    session: AsyncSession = Depends(get_session_dependency),
) -> UserRepository:
    return UserRepository(session)


def get_user_service(
    repo: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(repo)


def get_auth_service(
    repo: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(repo)


async def get_current_user_id(
    token: str = Depends(oauth2_scheme),
) -> str:
    payload = decode_token(token)
    if payload is None or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
        )
    user_id: str | None = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
    return user_id
