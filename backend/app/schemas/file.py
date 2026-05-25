from datetime import datetime

from pydantic import BaseModel


class FileResponse(BaseModel):
    file_id: int
    flow_file_id: int
    file_path: str
    file_name: str
    file_size: int
    file_type: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
