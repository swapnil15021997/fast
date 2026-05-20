from pydantic import BaseModel


class ChatMessageCreate(BaseModel):
    role: str
    content: str


class ChatMessageResponse(BaseModel):
    id: str
    chat_id: str
    role: str
    content: str
    created_at: str

    model_config = {"from_attributes": True}


class ChatCreate(BaseModel):
    flow_id: str
    title: str = ""


class ChatResponse(BaseModel):
    id: str
    flow_id: str
    user_id: str
    title: str
    created_at: str
    updated_at: str

    model_config = {"from_attributes": True}


class ChatDetailResponse(ChatResponse):
    messages: list[ChatMessageResponse]
