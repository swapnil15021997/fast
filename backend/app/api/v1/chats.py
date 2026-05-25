from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user_id, get_chat_service
from app.schemas.chat import (
    ChatCreate,
    ChatResponse,
    ChatDetailResponse,
    ChatMessageCreate,
    ChatMessageResponse,
    ChatResponseCreate,
)
from app.services.chat import ChatService

router = APIRouter()


@router.post("", response_model=ChatResponse, status_code=201)
async def create_chat(
    body: ChatCreate,
    user_id: int = Depends(get_current_user_id),
    chat_service: ChatService = Depends(get_chat_service),
) -> ChatResponse:
    return await chat_service.create(
        flow_id=body.flow_id, user_id=user_id, title=body.title
    )


@router.get("", response_model=list[ChatResponse])
async def list_chats(
    user_id: int = Depends(get_current_user_id),
    chat_service: ChatService = Depends(get_chat_service),
) -> list[ChatResponse]:
    return await chat_service.list_by_user(user_id)


@router.get("/{chat_id}", response_model=ChatDetailResponse)
async def get_chat(
    chat_id: int,
    user_id: int = Depends(get_current_user_id),
    chat_service: ChatService = Depends(get_chat_service),
) -> ChatDetailResponse:
    return await chat_service.get_by_id(chat_id)


@router.post("/{chat_id}/messages", response_model=ChatMessageResponse, status_code=201)
async def add_message(
    chat_id: int,
    body: ChatMessageCreate,
    user_id: int = Depends(get_current_user_id),
    chat_service: ChatService = Depends(get_chat_service),
) -> ChatMessageResponse:
    return await chat_service.add_message(chat_id, body.role, body.content)


@router.post("/{chat_id}/respond", response_model=ChatMessageResponse, status_code=201)
async def respond_chat(
    chat_id: int,
    body: ChatResponseCreate,
    user_id: int = Depends(get_current_user_id),
    chat_service: ChatService = Depends(get_chat_service),
) -> ChatMessageResponse:
    return await chat_service.respond(
        chat_id,
        body.prompt,
        model=body.model,
        file_ids=body.file_ids,
    )


@router.get("/{chat_id}/messages", response_model=list[ChatMessageResponse])
async def get_messages(
    chat_id: int,
    user_id: int = Depends(get_current_user_id),
    chat_service: ChatService = Depends(get_chat_service),
) -> list[ChatMessageResponse]:
    return await chat_service.get_messages(chat_id)
