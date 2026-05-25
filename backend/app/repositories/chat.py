from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.chat import Chat, ChatMessage
from datetime import datetime, timezone


class ChatRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, flow_id: int, user_id: int, title: str = "") -> Chat:
        chat = Chat(
            flow_id=flow_id,
            user_id=user_id,
            title=title,
        )
        self._session.add(chat)
        await self._session.flush()
        await self._session.refresh(chat)
        return chat

    async def get_by_id(self, chat_id: int) -> Chat | None:
        return await self._session.get(Chat, chat_id)

    async def get_by_id_with_messages(self, chat_id: int) -> Chat | None:
        result = await self._session.execute(
            select(Chat)
            .where(Chat.id == chat_id)
            .options(joinedload(Chat.messages))
        )
        return result.unique().scalar_one_or_none()

    async def list_by_flow(self, flow_id: int) -> list[Chat]:
        result = await self._session.execute(
            select(Chat).where(Chat.flow_id == flow_id).order_by(Chat.created_at.desc())
        )
        return list(result.scalars().all())

    async def list_by_user(self, user_id: int) -> list[Chat]:
        result = await self._session.execute(
            select(Chat).where(Chat.user_id == user_id).order_by(Chat.created_at.desc())
        )
        return list(result.scalars().all())

    async def add_message(self, chat_id: int, role: str, content: str) -> ChatMessage:
        msg = ChatMessage(
            chat_id=chat_id,
            role=role,
            content=content,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self._session.add(msg)
        await self._session.flush()
        return msg

    async def get_messages(self, chat_id: int) -> list[ChatMessage]:
        result = await self._session.execute(
            select(ChatMessage)
            .where(ChatMessage.chat_id == chat_id)
            .order_by(ChatMessage.created_at.asc())
        )
        return list(result.scalars().all())
