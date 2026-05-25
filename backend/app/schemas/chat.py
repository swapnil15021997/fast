from datetime import datetime

from pydantic import BaseModel


class ChatMessageCreate(BaseModel):
    role: str
    content: str


class ChatMessageResponse(BaseModel):
    id: int
    chat_id: int
    role: str
    content: str
    created_at: str

    model_config = {"from_attributes": True}


class ChatCreate(BaseModel):
    flow_id: int
    title: str = ""


class ChatResponse(BaseModel):
    id: int
    flow_id: int
    user_id: int
    title: str
    created_at: str
    updated_at: str

    model_config = {"from_attributes": True}


class ChatResponseCreate(BaseModel):
    prompt: str
    model: str | None = None
    file_ids: list[int] | None = None


class ChatDetailResponse(ChatResponse):
    messages: list[ChatMessageResponse]
