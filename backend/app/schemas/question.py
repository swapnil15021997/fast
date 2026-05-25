import json
from datetime import datetime

from pydantic import BaseModel, field_validator


class QuestionCreate(BaseModel):
    question_text: str
    question_is_last: bool = False
    question_parent_id: int | None = None
    question_button_json: list[str] | None = None


class QuestionUpdate(BaseModel):
    question_text: str | None = None
    question_is_last: bool | None = None
    question_is_delete: bool | None = None
    question_button_json: list[str] | None = None


class QuestionResponse(BaseModel):
    question_id: int
    question_text: str
    question_is_last: bool
    question_parent_id: int | None
    question_is_delete: bool
    question_flow_id: int
    question_button_json: list[str] | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

    @field_validator("question_button_json", mode="before")
    def parse_button_json(cls, value):
        if value is None:
            return None
        if isinstance(value, str):
            try:
                return json.loads(value)
            except ValueError:
                return [value]
        return value
