from fastapi import HTTPException, status

from app.repositories.user import UserRepository
from app.schemas.user import UserResponse


class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self._repo = repo

    async def get_by_id(self, user_id: str) -> UserResponse:
        user = await self._repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return UserResponse.model_validate(user)
