from datetime import datetime

from pydantic import BaseModel


class QuestionCreate(BaseModel):
    question_text: str
    question_is_last: bool = False
    question_parent_id: str | None = None
    question_button_json: str | None = None


class QuestionUpdate(BaseModel):
    question_text: str | None = None
    question_is_last: bool | None = None
    question_is_delete: bool | None = None
    question_button_json: str | None = None


class QuestionResponse(BaseModel):
    question_id: str
    question_text: str
    question_is_last: bool
    question_parent_id: str | None
    question_is_delete: bool
    question_flow_id: str
    question_button_json: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
