from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user_id, get_ai_service, get_file_repository
from app.schemas.ai import AIConversationRequest, AIConversationResponse
from app.services.ai import AIService
from app.repositories.file import FileRepository

router = APIRouter()


@router.post("/conversation", response_model=AIConversationResponse)
async def ai_conversation(
    body: AIConversationRequest,
    user_id: int = Depends(get_current_user_id),
    ai_service: AIService = Depends(get_ai_service),
    file_repo: FileRepository = Depends(get_file_repository),
) -> AIConversationResponse:
    prompt = body.prompt
    if body.file_ids:
        document_texts = []
        for file_id in body.file_ids:
            file = await file_repo.get_by_id(file_id)
            if file:
                try:
                    from asyncio import to_thread
                    from pathlib import Path

                    text = await to_thread(Path(file.file_path).read_text, encoding="utf-8")
                except Exception:
                    text = ""
                if text:
                    document_texts.append(f"Document {file.file_name}:\n{text}")
        if document_texts:
            prompt = "\n\n".join(document_texts) + "\n\nUser prompt:\n" + prompt

    response = await ai_service.chat(prompt, model=body.model)
    return AIConversationResponse(response=response, model=body.model)
