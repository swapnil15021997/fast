from fastapi import HTTPException, status

from app.core.security import hash_password
from app.repositories.user import UserRepository
from app.schemas.user import UserResponse


class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self._repo = repo

    async def create(
        self,
        email: str,
        password: str,
        name: str,
        is_superuser: bool = False,
    ) -> UserResponse:
        user = await self._repo.create(email, hash_password(password), name, is_superuser)
        return UserResponse.model_validate(user)

    async def list(self) -> list[UserResponse]:
        users = await self._repo.list()
        return [UserResponse.model_validate(user) for user in users]

    async def get_by_id(self, user_id: int) -> UserResponse:
        user = await self._repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return UserResponse.model_validate(user)

    async def update(self, user_id: int, **kwargs) -> UserResponse:
        user = await self._repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        cleaned = {}
        for key, value in kwargs.items():
            if value is None:
                continue
            if key == "password":
                cleaned["hashed_password"] = hash_password(value)
            else:
                cleaned[key] = value
        if not cleaned:
            return UserResponse.model_validate(user)
        user = await self._repo.update(user, **cleaned)
        return UserResponse.model_validate(user)

    async def delete(self, user_id: int) -> None:
        user = await self._repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        await self._repo.delete(user)
