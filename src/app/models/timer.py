from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, JSON, CheckConstraint, UniqueConstraint, Time, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, time, date, UTC
from typing import List, Optional
from enum import Enum
import uuid
from ..core.db.database import Base

class TimerType(str, Enum):
    COUNTDOWN = "countdown"
    COUNTUP = "countup"
    STOPWATCH = "stopwatch"

class ChimeType(str, Enum):
    NONE = "none"
    BELL = "bell"
    CHIME = "chime"
    ALARM = "alarm"
    CUSTOM = "custom"

class FlashType(str, Enum):
    NONE = "none"
    SINGLE = "single"
    CONTINUOUS = "continuous"
    SLOW_BLINK = "slow_blink"
    FAST_BLINK = "fast_blink"

class Timer(Base):
    __tablename__ = "timers"

    # Fields with NO defaults (required for dataclass compatibility)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)

    # Primary Key (has init=False, so doesn't affect dataclass ordering)
    id: Mapped[int] = mapped_column("id", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False)

    # All fields with defaults (including nullable fields and explicit defaults)
    display_id: Mapped[int | None] = mapped_column(ForeignKey("displays.id"), nullable=True, index=True, default=None)
    speaker: Mapped[str | None] = mapped_column(String(255), nullable=True, default=None)
    notes: Mapped[str | None] = mapped_column(String(1000), nullable=True, default=None)

    uuid: Mapped[str] = mapped_column(String(36), default_factory=lambda: str(uuid.uuid4()), unique=True, index=True)
    
    # Start Configuration
    scheduled_start_time: Mapped[time | None] = mapped_column(Time, nullable=True, default=None)
    scheduled_start_date: Mapped[date | None] = mapped_column(Date, nullable=True, default=None)
    is_manual_start: Mapped[bool] = mapped_column(default=True)
    
    # Duration Configuration (stored in seconds for precision)
    duration_seconds: Mapped[int | None] = mapped_column(nullable=True, default=600)  # 10 minutes default
    
    # Timer Type and Configuration
    timer_type: Mapped[TimerType] = mapped_column(default=TimerType.COUNTDOWN)
    
    # Current State
    is_active: Mapped[bool] = mapped_column(default=False)
    is_paused: Mapped[bool] = mapped_column(default=False)
    is_finished: Mapped[bool] = mapped_column(default=False)
    is_stopped: Mapped[bool] = mapped_column(default=False)
    current_time_seconds: Mapped[int] = mapped_column(default=0)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, default=None)
    paused_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, default=None)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, default=None)
    
    # Display Configuration
    show_title: Mapped[bool] = mapped_column(default=True)
    show_speaker: Mapped[bool] = mapped_column(default=True)
    show_notes: Mapped[bool] = mapped_column(default=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    is_deleted: Mapped[bool] = mapped_column(default=False, index=True)