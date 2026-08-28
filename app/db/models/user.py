import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, UUID
from app.db.database import Base

class User(Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
