from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field

from ..core.schemas import TimestampSchema


class PlanFeatureBase(BaseModel):
    plan_id: Annotated[int, Field(examples=[1])]
    feature_key: Annotated[str, Field(examples=["max_rooms"])]
    value: Annotated[str, Field(examples=["3"])]


class PlanFeature(TimestampSchema, PlanFeatureBase):
    pass


class PlanFeatureRead(PlanFeatureBase):
    id: int
    created_at: datetime


class PlanFeatureCreate(PlanFeatureBase):
    pass


class PlanFeatureCreateInternal(PlanFeatureCreate):
    pass


class PlanFeatureUpdate(BaseModel):
    plan_id: int | None = None
    feature_key: str | None = None
    value: str | None = None


class PlanFeatureUpdateInternal(PlanFeatureUpdate):
    updated_at: datetime


class PlanFeatureDelete(BaseModel):
    pass
