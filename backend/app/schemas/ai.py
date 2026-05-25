from pydantic import BaseModel


class AIConversationRequest(BaseModel):
    prompt: str
    model: str | None = None
    file_ids: list[int] | None = None


class AIConversationResponse(BaseModel):
    response: str
    model: str | None = None
