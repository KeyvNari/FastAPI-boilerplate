from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from ..core.schemas import TimestampSchema, UUIDSchema


class SubscriptionBase(BaseModel):
    provider: Annotated[str, Field(examples=["stripe"])]
    provider_subscription_id: Annotated[str, Field(examples=["sub_1234567890"])]
    status: Annotated[str, Field(examples=["active", "canceled", "past_due"])]
    current_period_end: datetime


class Subscription(SubscriptionBase, UUIDSchema, TimestampSchema):
    user_id: UUID


class SubscriptionRead(SubscriptionBase, UUIDSchema, TimestampSchema):
    id: UUID
    user_id: UUID
    created_at: datetime | None


class SubscriptionCreate(SubscriptionBase):
    model_config = ConfigDict(extra="forbid")

    user_id: UUID


class SubscriptionUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    provider: str | None = None
    provider_subscription_id: str | None = None
    status: str | None = None
    current_period_end: datetime | None = None


class SubscriptionUpdateInternal(SubscriptionUpdate):
    updated_at: datetime | None = None
