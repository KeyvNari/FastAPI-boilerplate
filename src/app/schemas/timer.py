from datetime import datetime, time, date
from typing import Annotated
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from ..core.schemas import PersistentDeletion, TimestampSchema


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


class TimerBase(BaseModel):
    room_id: int
    title: Annotated[str, Field(min_length=1, max_length=255)]
    display_id: Annotated[int | None, Field(default=None)]
    speaker: Annotated[str | None, Field(max_length=255, default=None)]
    notes: Annotated[str | None, Field(max_length=1000, default=None)]
    scheduled_start_time: Annotated[time | None, Field(default=None)]
    scheduled_start_date: Annotated[date | None, Field(default=None)]
    is_manual_start: Annotated[bool, Field(default=True)]
    duration_seconds: Annotated[int | None, Field(default=600)]
    timer_type: Annotated[TimerType, Field(default=TimerType.COUNTDOWN)]
    show_title: Annotated[bool, Field(default=True)]
    show_speaker: Annotated[bool, Field(default=True)]
    show_notes: Annotated[bool, Field(default=False)]


class Timer(TimestampSchema, TimerBase, PersistentDeletion):
    room_id: int
    uuid: str
    is_active: bool
    is_paused: bool
    is_finished: bool
    is_stopped: bool
    current_time_seconds: int
    started_at: datetime | None
    paused_at: datetime | None
    completed_at: datetime | None


class TimerRead(BaseModel):
    id: int
    room_id: int
    title: str
    display_id: int | None
    speaker: str | None
    notes: str | None
    uuid: str
    scheduled_start_time: time | None
    scheduled_start_date: date | None
    is_manual_start: bool
    duration_seconds: int | None
    timer_type: TimerType
    is_active: bool
    is_paused: bool
    is_finished: bool
    is_stopped: bool
    current_time_seconds: int
    started_at: datetime | None
    paused_at: datetime | None
    completed_at: datetime | None
    show_title: bool
    show_speaker: bool
    show_notes: bool
    created_at: datetime
    updated_at: datetime | None
    deleted_at: datetime | None
    is_deleted: bool


class TimerCreate(TimerBase):
    model_config = ConfigDict(extra="forbid")


class TimerCreateInternal(TimerCreate):
    room_id: int
    uuid: str
    is_active: bool = False
    is_paused: bool = False
    is_finished: bool = False
    is_stopped: bool = False
    current_time_seconds: int = 0
    started_at: datetime | None = None
    paused_at: datetime | None = None
    completed_at: datetime | None = None


class TimerUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Annotated[str | None, Field(min_length=1, max_length=255, default=None)]
    display_id: Annotated[int | None, Field(default=None)]
    speaker: Annotated[str | None, Field(max_length=255, default=None)]
    notes: Annotated[str | None, Field(max_length=1000, default=None)]
    scheduled_start_time: Annotated[time | None, Field(default=None)]
    scheduled_start_date: Annotated[date | None, Field(default=None)]
    is_manual_start: Annotated[bool | None, Field(default=None)]
    duration_seconds: Annotated[int | None, Field(default=None)]
    timer_type: Annotated[TimerType | None, Field(default=None)]
    show_title: Annotated[bool | None, Field(default=None)]
    show_speaker: Annotated[bool | None, Field(default=None)]
    show_notes: Annotated[bool | None, Field(default=None)]


class TimerUpdateInternal(TimerUpdate):
    updated_at: datetime


class TimerDelete(BaseModel):
    model_config = ConfigDict(extra="forbid")

    is_deleted: bool
    deleted_at: datetime
