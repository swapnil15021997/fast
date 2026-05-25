from asyncio import to_thread
from pathlib import Path

from fastapi import HTTPException, status

from app.repositories.chat import ChatRepository
from app.repositories.file import FileRepository
from app.schemas.chat import ChatResponse, ChatDetailResponse, ChatMessageResponse
from app.services.ai import AIService


def _serialize_chat(chat):
    return {
        "id": chat.id,
        "flow_id": chat.flow_id,
        "user_id": chat.user_id,
        "title": chat.title,
        "created_at": chat.created_at.isoformat() if hasattr(chat.created_at, "isoformat") else str(chat.created_at),
        "updated_at": chat.updated_at.isoformat() if hasattr(chat.updated_at, "isoformat") else str(chat.updated_at),
    }


class ChatService:
    def __init__(
        self,
        repo: ChatRepository,
        file_repo: FileRepository,
        ai_service: AIService,
    ) -> None:
        self._repo = repo
        self._file_repo = file_repo
        self._ai_service = ai_service

    async def create(self, flow_id: int, user_id: int, title: str = "") -> ChatResponse:
        chat = await self._repo.create(flow_id, user_id, title)
        return ChatResponse.model_validate(_serialize_chat(chat))

    async def get_by_id(self, chat_id: int) -> ChatDetailResponse:
        chat = await self._repo.get_by_id_with_messages(chat_id)
        if not chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat not found",
            )
        return ChatDetailResponse(
            **_serialize_chat(chat),
            messages=[ChatMessageResponse.model_validate(m) for m in chat.messages],
        )

    async def list_by_flow(self, flow_id: int) -> list[ChatResponse]:
        chats = await self._repo.list_by_flow(flow_id)
        return [ChatResponse.model_validate(_serialize_chat(c)) for c in chats]

    async def list_by_user(self, user_id: int) -> list[ChatResponse]:
        chats = await self._repo.list_by_user(user_id)
        return [ChatResponse.model_validate(_serialize_chat(c)) for c in chats]

    async def _load_file_content(self, file_path: str) -> str:
        try:
            return await to_thread(Path(file_path).read_text, encoding="utf-8")
        except Exception:
            return ""

    async def respond(
        self,
        chat_id: int,
        prompt: str,
        model: str | None = None,
        file_ids: list[int] | None = None,
    ) -> ChatMessageResponse:
        chat = await self._repo.get_by_id(chat_id)
        if not chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat not found",
            )

        context_texts = []
        if file_ids:
            for file_id in file_ids:
                file = await self._file_repo.get_by_id(file_id)
                if file:
                    text = await self._load_file_content(file.file_path)
                    if text:
                        context_texts.append(f"Document {file.file_name}:\n{text}")

        if context_texts:
            prompt = "\n\n".join(context_texts) + "\n\nUser prompt:\n" + prompt

        await self._repo.add_message(chat_id, "user", prompt)
        ai_response = await self._ai_service.chat(prompt, model=model)
        msg = await self._repo.add_message(chat_id, "assistant", ai_response)
        return ChatMessageResponse.model_validate(msg)

    async def add_message(self, chat_id: int, role: str, content: str) -> ChatMessageResponse:
        chat = await self._repo.get_by_id(chat_id)
        if not chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat not found",
            )
        msg = await self._repo.add_message(chat_id, role, content)
        return ChatMessageResponse.model_validate(msg)

    async def get_messages(self, chat_id: int) -> list[ChatMessageResponse]:
        chat = await self._repo.get_by_id(chat_id)
        if not chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat not found",
            )
        messages = await self._repo.get_messages(chat_id)
        return [ChatMessageResponse.model_validate(m) for m in messages]
