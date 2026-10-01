from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.services.database import Base


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(50), primary_key=True)
    email: Mapped[str | None] = mapped_column(String(100), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))
    last_login: Mapped[datetime | None] = mapped_column(DateTime)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    profile_name: Mapped[str | None] = mapped_column(String(100))