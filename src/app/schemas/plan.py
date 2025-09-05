from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field

from ..core.schemas import TimestampSchema


class PlanBase(BaseModel):
    name: Annotated[str, Field(examples=["FREE"])]
    price_cents: Annotated[int, Field(examples=[0])]
    interval: Annotated[str, Field(examples=["month"])]
    description: str | None = None


class Plan(TimestampSchema, PlanBase):
    pass


class PlanRead(PlanBase):
    id: int
    created_at: datetime


class PlanCreate(PlanBase):
    pass


class PlanCreateInternal(PlanCreate):
    pass


class PlanUpdate(BaseModel):
    name: str | None = None
    price_cents: int | None = None
    interval: str | None = None
    description: str | None = None


class PlanUpdateInternal(PlanUpdate):
    updated_at: datetime


class PlanDelete(BaseModel):
    pass
