from datetime import UTC, datetime

from sqlalchemy import DateTime, String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base


class Plan(Base):
    __tablename__ = "plans"

    id: Mapped[int] = mapped_column("id", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    price_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    interval: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    is_deleted: Mapped[bool] = mapped_column(default=False, index=True)
