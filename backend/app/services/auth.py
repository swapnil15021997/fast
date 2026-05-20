from fastapi import HTTPException, status

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.repositories.user import UserRepository
from app.schemas.auth import TokenResponse


class AuthService:
    def __init__(self, repo: UserRepository) -> None:
        self._repo = repo

    async def register(self, email: str, password: str, name: str) -> TokenResponse:
        existing = await self._repo.get_by_email(email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )
        hashed = hash_password(password)
        user = await self._repo.create(email, hashed, name)
        return await self._generate_tokens(user.id)

    async def login(self, email: str, password: str) -> TokenResponse:
        user = await self._repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is deactivated",
            )
        return await self._generate_tokens(user.id)

    async def refresh(self, refresh_token: str) -> TokenResponse:
        payload = decode_token(refresh_token)
        if payload is None or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token",
            )
        stored = await self._repo.get_refresh_token(refresh_token)
        if stored is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has been revoked",
            )
        await self._repo.revoke_refresh_token(stored)
        return await self._generate_tokens(payload["sub"])

    async def _generate_tokens(self, user_id: str) -> TokenResponse:
        access = create_access_token(user_id)
        refresh = create_refresh_token(user_id)
        await self._repo.save_refresh_token(user_id, refresh)
        return TokenResponse(access_token=access, refresh_token=refresh)
