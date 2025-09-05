from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from ..core.schemas import PersistentDeletion, TimestampSchema


class DisplayBase(BaseModel):
    name: Annotated[str, Field(default="Untitled Display")]
    logo_image: Annotated[str | None, Field(default=None)]
    logo_size_percent: Annotated[int | None, Field(default=60)]
    logo_position: Annotated[str | None, Field(default="top_left")]
    timer_format: Annotated[str | None, Field(default="hhh:mmm:ss")]
    timer_font_family: Annotated[str | None, Field(default="Inter")]
    timer_color: Annotated[str | None, Field(default=None)]
    time_of_day_color: Annotated[str | None, Field(default=None)]
    timer_text_style: Annotated[str | None, Field(default="default")]
    timer_size_percent: Annotated[int | None, Field(default=100)]
    timer_position: Annotated[str | None, Field(default="center")]
    auto_hide_completed: Annotated[bool, Field(default=False)]
    clock_format: Annotated[str | None, Field(default="browser_default")]
    clock_font_family: Annotated[str | None, Field(default="Inter")]
    clock_color: Annotated[str | None, Field(default=None)]
    clock_visible: Annotated[bool, Field(default=True)]
    message_font_family: Annotated[str | None, Field(default="Inter")]
    message_color: Annotated[str | None, Field(default=None)]
    title_display_location: Annotated[str | None, Field(default="header")]
    speaker_display_location: Annotated[str | None, Field(default="footer")]
    next_cue_display_location: Annotated[str | None, Field(default="header")]
    header_font_family: Annotated[str | None, Field(default="Inter")]
    header_color: Annotated[str | None, Field(default=None)]
    footer_font_family: Annotated[str | None, Field(default="Inter")]
    footer_color: Annotated[str | None, Field(default=None)]
    theme_name: Annotated[str | None, Field(default="default")]
    text_style: Annotated[str | None, Field(default="default")]
    background_type: Annotated[str | None, Field(default="color")]
    background_color: Annotated[str | None, Field(default=None)]
    background_image: Annotated[str | None, Field(default=None)]
    background_preset: Annotated[str | None, Field(default=None)]
    progress_style: Annotated[str | None, Field(default="bottom_bar")]
    progress_color_main: Annotated[str | None, Field(default=None)]
    progress_color_secondary: Annotated[str | None, Field(default=None)]
    progress_color_tertiary: Annotated[str | None, Field(default=None)]


class Display(TimestampSchema, DisplayBase, PersistentDeletion):
    created_by_user_id: int


class DisplayRead(BaseModel):
    id: int
    name: str
    logo_image: str | None
    logo_size_percent: int | None
    logo_position: str | None
    timer_format: str | None
    timer_font_family: str | None
    timer_color: str | None
    time_of_day_color: str | None
    timer_text_style: str | None
    timer_size_percent: int | None
    timer_position: str | None
    auto_hide_completed: bool
    clock_format: str | None
    clock_font_family: str | None
    clock_color: str | None
    clock_visible: bool
    message_font_family: str | None
    message_color: str | None
    title_display_location: str | None
    speaker_display_location: str | None
    next_cue_display_location: str | None
    header_font_family: str | None
    header_color: str | None
    footer_font_family: str | None
    footer_color: str | None
    theme_name: str | None
    text_style: str | None
    background_type: str | None
    background_color: str | None
    background_image: str | None
    background_preset: str | None
    progress_style: str | None
    progress_color_main: str | None
    progress_color_secondary: str | None
    progress_color_tertiary: str | None
    created_by_user_id: int
    created_at: datetime


class DisplayCreate(DisplayBase):
    model_config = ConfigDict(extra="forbid")


class DisplayCreateInternal(DisplayCreate):
    created_by_user_id: int


class DisplayUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: Annotated[str | None, Field(default=None)]
    logo_image: Annotated[str | None, Field(default=None)]
    logo_size_percent: Annotated[int | None, Field(default=None)]
    logo_position: Annotated[str | None, Field(default=None)]
    timer_format: Annotated[str | None, Field(default=None)]
    timer_font_family: Annotated[str | None, Field(default=None)]
    timer_color: Annotated[str | None, Field(default=None)]
    time_of_day_color: Annotated[str | None, Field(default=None)]
    timer_text_style: Annotated[str | None, Field(default=None)]
    timer_size_percent: Annotated[int | None, Field(default=None)]
    timer_position: Annotated[str | None, Field(default=None)]
    auto_hide_completed: Annotated[bool | None, Field(default=None)]
    clock_format: Annotated[str | None, Field(default=None)]
    clock_font_family: Annotated[str | None, Field(default=None)]
    clock_color: Annotated[str | None, Field(default=None)]
    clock_visible: Annotated[bool | None, Field(default=None)]
    message_font_family: Annotated[str | None, Field(default=None)]
    message_color: Annotated[str | None, Field(default=None)]
    title_display_location: Annotated[str | None, Field(default=None)]
    speaker_display_location: Annotated[str | None, Field(default=None)]
    next_cue_display_location: Annotated[str | None, Field(default=None)]
    header_font_family: Annotated[str | None, Field(default=None)]
    header_color: Annotated[str | None, Field(default=None)]
    footer_font_family: Annotated[str | None, Field(default=None)]
    footer_color: Annotated[str | None, Field(default=None)]
    theme_name: Annotated[str | None, Field(default=None)]
    text_style: Annotated[str | None, Field(default=None)]
    background_type: Annotated[str | None, Field(default=None)]
    background_color: Annotated[str | None, Field(default=None)]
    background_image: Annotated[str | None, Field(default=None)]
    background_preset: Annotated[str | None, Field(default=None)]
    progress_style: Annotated[str | None, Field(default=None)]
    progress_color_main: Annotated[str | None, Field(default=None)]
    progress_color_secondary: Annotated[str | None, Field(default=None)]
    progress_color_tertiary: Annotated[str | None, Field(default=None)]


class DisplayUpdateInternal(DisplayUpdate):
    updated_at: datetime


class DisplayDelete(BaseModel):
    model_config = ConfigDict(extra="forbid")

    is_deleted: bool
    deleted_at: datetime
