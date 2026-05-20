from pydantic import BaseModel


class UserAITokenResponse(BaseModel):
    id: str
    user_id: str
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
