from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID
from datetime import datetime

from app.db.database import Base


class User(Base):
    __tablename__ = "url"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        relationship = relationship("user")
    )

    target_url: Mapped[str]
    short_url: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

