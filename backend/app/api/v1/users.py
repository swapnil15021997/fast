from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user_id, get_user_service
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user import UserService

router = APIRouter()


@router.post("", response_model=UserResponse, status_code=201)
async def create_user(
    body: UserCreate,
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    return await user_service.create(
        email=body.email,
        password=body.password,
        name=body.name,
    )


@router.get("", response_model=list[UserResponse])
async def list_users(
    current_user_id: int = Depends(get_current_user_id),
    user_service: UserService = Depends(get_user_service),
) -> list[UserResponse]:
    return await user_service.list()


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user_id: int = Depends(get_current_user_id),
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    return await user_service.get_by_id(user_id)


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    body: UserUpdate,
    current_user_id: int = Depends(get_current_user_id),
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    return await user_service.update(
        user_id,
        email=body.email,
        password=body.password,
        name=body.name,
        is_active=body.is_active,
        is_superuser=body.is_superuser,
    )


@router.get("/me", response_model=UserResponse)
async def get_me(
    user_id: int = Depends(get_current_user_id),
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    return await user_service.get_by_id(user_id)


@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    current_user_id: int = Depends(get_current_user_id),
    user_service: UserService = Depends(get_user_service),
) -> None:
    await user_service.delete(user_id)
