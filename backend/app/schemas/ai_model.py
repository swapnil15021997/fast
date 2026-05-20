from pydantic import BaseModel


class AIModelResponse(BaseModel):
    ai_id: str
    ai_name: str

    model_config = {"from_attributes": True}
