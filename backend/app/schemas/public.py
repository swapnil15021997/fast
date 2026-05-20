from pydantic import BaseModel


class PublicShareResponse(BaseModel):
    public_token: str
    share_url: str
