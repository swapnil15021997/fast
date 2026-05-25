from pydantic import BaseModel


class AIModelCreate(BaseModel):
    ai_name: str


class AIModelUpdate(BaseModel):
    ai_name: str | None = None


class AIModelResponse(BaseModel):
    ai_id: int
    ai_name: str

    model_config = {"from_attributes": True}
