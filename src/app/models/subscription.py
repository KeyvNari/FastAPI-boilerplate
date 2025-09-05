import uuid as uuid_pkg
from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] =mapped_column("id", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False)

    user_id: Mapped[uuid_pkg.UUID] = mapped_column(ForeignKey("user.uuid"), nullable=False)

    provider: Mapped[str] = mapped_column(String, nullable=False)
    provider_subscription_id: Mapped[str] = mapped_column(String, nullable=False)

    status: Mapped[str] = mapped_column(String, nullable=False)  # active, canceled, past_due

    current_period_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    is_deleted: Mapped[bool] = mapped_column(default=False, index=True)