from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token
from app.db.session import get_session
from app.repositories.user import UserRepository
from app.repositories.flow import FlowRepository
from app.repositories.question import QuestionRepository
from app.repositories.file import FileRepository
from app.repositories.ai_model import AIModelRepository
from app.repositories.token import UserAITokenRepository
from app.repositories.chat import ChatRepository
from app.repositories.customer import CustomerRepository
from app.services.auth import AuthService
from app.services.user import UserService
from app.services.ai import AIService
from app.services.flow import FlowService
from app.services.question import QuestionService
from app.services.file import FileService
from app.services.token import TokenService
from app.services.chat import ChatService
from app.services.public import PublicService
from app.services.customer import CustomerService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_session_dependency() -> AsyncSession:
    async for session in get_session():
        yield session


def get_user_repository(
    session: AsyncSession = Depends(get_session_dependency),
) -> UserRepository:
    return UserRepository(session)


def get_flow_repository(
    session: AsyncSession = Depends(get_session_dependency),
) -> FlowRepository:
    return FlowRepository(session)


def get_question_repository(
    session: AsyncSession = Depends(get_session_dependency),
) -> QuestionRepository:
    return QuestionRepository(session)


def get_file_repository(
    session: AsyncSession = Depends(get_session_dependency),
) -> FileRepository:
    return FileRepository(session)


def get_ai_model_repository(
    session: AsyncSession = Depends(get_session_dependency),
) -> AIModelRepository:
    return AIModelRepository(session)


def get_token_repository(
    session: AsyncSession = Depends(get_session_dependency),
) -> UserAITokenRepository:
    return UserAITokenRepository(session)


def get_chat_repository(
    session: AsyncSession = Depends(get_session_dependency),
) -> ChatRepository:
    return ChatRepository(session)


def get_customer_repository(
    session: AsyncSession = Depends(get_session_dependency),
) -> CustomerRepository:
    return CustomerRepository(session)


def get_user_service(
    repo: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(repo)


def get_auth_service(
    repo: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(repo)


def get_flow_service(
    repo: FlowRepository = Depends(get_flow_repository),
) -> FlowService:
    return FlowService(repo)


def get_question_service(
    repo: QuestionRepository = Depends(get_question_repository),
) -> QuestionService:
    return QuestionService(repo)


def get_file_service(
    repo: FileRepository = Depends(get_file_repository),
) -> FileService:
    return FileService(repo)


def get_ai_model_service() -> AIModelRepository:
    raise NotImplementedError("Use get_ai_model_repository directly")


def get_token_service(
    repo: UserAITokenRepository = Depends(get_token_repository),
) -> TokenService:
    return TokenService(repo)


def get_ai_service() -> AIService:
    return AIService()


def get_chat_service(
    repo: ChatRepository = Depends(get_chat_repository),
    file_repo: FileRepository = Depends(get_file_repository),
    ai_service: AIService = Depends(get_ai_service),
) -> ChatService:
    return ChatService(repo, file_repo, ai_service)


def get_public_service(
    repo: FlowRepository = Depends(get_flow_repository),
) -> PublicService:
    return PublicService(repo)


def get_customer_service(
    repo: CustomerRepository = Depends(get_customer_repository),
) -> CustomerService:
    return CustomerService(repo)


async def get_current_user_id(
    token: str = Depends(oauth2_scheme),
) -> int:
    payload = decode_token(token)
    if payload is None or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
        )
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
    try:
        return int(user_id)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
