from pydantic import BaseModel


class UserAITokenResponse(BaseModel):
    id: str
    user_id: str
    ai_model_id: str | None
    tokens_used: int
    tokens_limit: int
    period_start: str
    period_end: str

    model_config = {"from_attributes": True}


class TokenUsageResponse(BaseModel):
    tokens_used: int
    tokens_limit: int
    tokens_remaining: int
    period_start: str
    period_end: str


class TokenUpdate(BaseModel):
    ai_model_id: str | None = None
    tokens_limit: int | None = None
