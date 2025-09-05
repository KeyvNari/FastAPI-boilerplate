from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base


class PlanFeature(Base):
    __tablename__ = "plan_features"

    id: Mapped[int] = mapped_column("id", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False)
    plan_id: Mapped[int] = mapped_column(ForeignKey("plans.id"), nullable=False)
    feature_key: Mapped[str] = mapped_column(String, nullable=False)
    value: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    is_deleted: Mapped[bool] = mapped_column(default=False, index=True)
