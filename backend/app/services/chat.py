from fastapi import HTTPException, status

from app.repositories.chat import ChatRepository
from app.schemas.chat import ChatResponse, ChatDetailResponse, ChatMessageResponse


class ChatService:
    def __init__(self, repo: ChatRepository) -> None:
        self._repo = repo

    async def create(self, flow_id: str, user_id: str, title: str = "") -> ChatResponse:
        chat = await self._repo.create(flow_id, user_id, title)
        return ChatResponse.model_validate(chat)

    async def get_by_id(self, chat_id: str) -> ChatDetailResponse:
        chat = await self._repo.get_by_id_with_messages(chat_id)
        if not chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat not found",
            )
        return ChatDetailResponse(
            id=chat.id,
            flow_id=chat.flow_id,
            user_id=chat.user_id,
            title=chat.title,
            created_at=chat.created_at.isoformat() if hasattr(chat.created_at, 'isoformat') else str(chat.created_at),
            updated_at=chat.updated_at.isoformat() if hasattr(chat.updated_at, 'isoformat') else str(chat.updated_at),
            messages=[ChatMessageResponse.model_validate(m) for m in chat.messages],
        )

    async def list_by_flow(self, flow_id: str) -> list[ChatResponse]:
        chats = await self._repo.list_by_flow(flow_id)
        return [ChatResponse.model_validate(c) for c in chats]

    async def list_by_user(self, user_id: str) -> list[ChatResponse]:
        chats = await self._repo.list_by_user(user_id)
        return [ChatResponse.model_validate(c) for c in chats]

    async def add_message(self, chat_id: str, role: str, content: str) -> ChatMessageResponse:
        chat = await self._repo.get_by_id(chat_id)
        if not chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat not found",
            )
        msg = await self._repo.add_message(chat_id, role, content)
        return ChatMessageResponse.model_validate(msg)

    async def get_messages(self, chat_id: str) -> list[ChatMessageResponse]:
        chat = await self._repo.get_by_id(chat_id)
        if not chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat not found",
            )
        messages = await self._repo.get_messages(chat_id)
        return [ChatMessageResponse.model_validate(m) for m in messages]
