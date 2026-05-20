from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
