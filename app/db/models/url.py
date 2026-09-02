from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UUID, ForeignKey, DateTime
from datetime import datetime, timezone

from app.db.database import Base


class Url(Base):
    __tablename__ = "url"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.id"),
    )

    target_url: Mapped[str]
    short_code: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    clicks: Mapped[int] = mapped_column(default=0)

