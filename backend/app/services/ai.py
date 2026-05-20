import logging

from fastapi import HTTPException, status

from app.ai.chat import get_chat_response
from app.ai.client import openai_client
from app.ai.embeddings import get_embedding

logger = logging.getLogger(__name__)


class AIService:
    def __init__(self) -> None:
        self._client = openai_client

    async def chat(self, prompt: str, model: str | None = None) -> str:
        try:
            return await get_chat_response(prompt, model=model)
        except Exception as exc:
            logger.exception("AI chat failed")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="AI service unavailable",
            ) from exc

    async def embed(self, text: str) -> list[float]:
        try:
            return await get_embedding(text)
        except Exception as exc:
            logger.exception("AI embedding failed")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="AI embedding service unavailable",
            ) from exc
