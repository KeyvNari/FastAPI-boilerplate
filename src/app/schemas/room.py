from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from ..core.schemas import PersistentDeletion, TimestampSchema


class RoomBase(BaseModel):
    created_by_user_id: int
    name: Annotated[str, Field(min_length=1, max_length=50)]
    time_zone: Annotated[str | None, Field(max_length=50, default=None)]
    description: Annotated[str | None, Field(max_length=1000, default=None)]
    is_active: Annotated[bool, Field(default=True)]


class Room(TimestampSchema, RoomBase, PersistentDeletion):
    created_by_user_id: int


class RoomRead(BaseModel):
    id: int
    created_by_user_id: int
    name: str
    description: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime | None
    deleted_at: datetime | None
    is_deleted: bool


class RoomCreate(RoomBase):
    model_config = ConfigDict(extra="forbid")


class RoomCreateInternal(RoomCreate):
    created_by_user_id: int


class RoomUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: Annotated[str | None, Field(min_length=1, max_length=50, default=None)]
    description: Annotated[str | None, Field(max_length=1000, default=None)]
    time_zone: Annotated[str | None, Field(max_length=50, default=None)]
    is_active: Annotated[bool | None, Field(default=None)]


class RoomUpdateInternal(RoomUpdate):
    updated_at: datetime


class RoomDelete(BaseModel):
    model_config = ConfigDict(extra="forbid")

    is_deleted: bool
    deleted_at: datetime
