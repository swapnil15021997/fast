from pydantic import BaseModel


class AIModelCreate(BaseModel):
    ai_name: str


class AIModelUpdate(BaseModel):
    ai_name: str | None = None


class AIModelResponse(BaseModel):
    ai_id: str
    ai_name: str

    model_config = {"from_attributes": True}
