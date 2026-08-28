from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UUID, ForeignKey
from datetime import datetime

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
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    clicks: Mapped[int] = mapped_column(default=0)

