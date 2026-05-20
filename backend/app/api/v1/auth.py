from fastapi import APIRouter, Depends

from app.core.dependencies import get_auth_service
from app.schemas.auth import RefreshRequest, TokenResponse, UserLogin
from app.schemas.user import UserCreate
from app.services.auth import AuthService

router = APIRouter()


@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(
    body: UserCreate,
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    return await auth_service.register(
        email=body.email,
        password=body.password,
        name=body.name,
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    body: UserLogin,
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    return await auth_service.login(email=body.email, password=body.password)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    body: RefreshRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    return await auth_service.refresh(refresh_token=body.refresh_token)
