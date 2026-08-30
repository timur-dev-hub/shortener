from pydantic import BaseModel, HttpUrl, computed_field, Field, ConfigDict, TypeAdapter
from datetime import datetime
from typing import Annotated, List

from app.core.config import settings

http_url_adapter = TypeAdapter(HttpUrl)
ShortCode = Annotated[str, Field(min_length=12, max_length=12)]

class LinkCreate(BaseModel):
    target_url: HttpUrl

class LinkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    target_url: HttpUrl

    short_code: str = Field(exclude=True)

    created_at: datetime
    clicks: int

    @computed_field
    @property
    def short_url(self) -> HttpUrl:
        return http_url_adapter.validate_python(
            f"{settings.SERVICE_DOMAIN}r/{self.short_code}"
        )


class UrlsResponse(BaseModel):
    links: List[LinkResponse]

