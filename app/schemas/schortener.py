from pydantic import BaseModel, HttpUrl
from datetime import datetime


class LinkCreate(BaseModel):
    target_url: HttpUrl

class LinkResponse(LinkCreate):
    id: int
    target_url: HttpUrl
    short_url: HttpUrl
    created_at: datetime

