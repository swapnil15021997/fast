from datetime import datetime

from pydantic import BaseModel


class FlowCreate(BaseModel):
    flow_name: str


class FlowUpdate(BaseModel):
    flow_name: str | None = None


class FlowResponse(BaseModel):
    flow_id: str
    flow_name: str
    flow_user_id: str
    flow_is_delete: bool
    is_public: bool
    public_token: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class FlowPublicResponse(BaseModel):
    flow_id: str
    flow_name: str
    created_at: datetime

    model_config = {"from_attributes": True}
