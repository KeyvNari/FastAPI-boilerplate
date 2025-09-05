from datetime import UTC, datetime

from sqlalchemy import DateTime, String, Integer, Text,ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base


class Display(Base):
   __tablename__ = "displays"

   id: Mapped[int] = mapped_column("id", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False)
   created_by_user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), index=True)
   name: Mapped[str] = mapped_column(String, nullable=False, default="Untitled Display")
   
   # Logo Configuration
   logo_image: Mapped[str | None] = mapped_column(String, nullable=True, default=None) # base64
   logo_size_percent: Mapped[int | None] = mapped_column(nullable=True, default=60)
   logo_position: Mapped[str | None] = mapped_column(String, nullable=True, default="top_left")  # top_left, top_right, bottom_left, bottom_right
   
   # Timer Configuration
   timer_format: Mapped[str | None] = mapped_column(String, nullable=True, default="hhh:mmm:ss")  # hhh:mm:ss, mm:ss, ss
   timer_font_family: Mapped[str | None] = mapped_column(String, nullable=True, default="Inter")
   timer_color: Mapped[str | None] = mapped_column(String, nullable=True, default=None)
   time_of_day_color: Mapped[str | None] = mapped_column(String, nullable=True, default=None)
   timer_text_style: Mapped[str | None] = mapped_column(String, nullable=True, default="default")  # default, outline, shadow
   timer_size_percent: Mapped[int | None] = mapped_column(default=100)
   timer_position: Mapped[str | None] = mapped_column(default="center")
   auto_hide_completed: Mapped[bool] = mapped_column(default=False)

   # Clock Configuration
   clock_format: Mapped[str | None] = mapped_column(String, nullable=True, default="browser_default")
   clock_font_family: Mapped[str | None] = mapped_column(String, nullable=True, default="Inter")
   clock_color: Mapped[str | None] = mapped_column(String, nullable=True, default=None)
   clock_visible: Mapped[bool] = mapped_column(default=True)
   
   # Message Configuration
   message_font_family: Mapped[str | None] = mapped_column(String, nullable=True, default="Inter")
   message_color: Mapped[str | None] = mapped_column(String, nullable=True, default=None)
   
   # Header/Footer Configuration
   title_display_location: Mapped[str | None] = mapped_column(String, nullable=True, default="header")  # header, footer, hidden
   speaker_display_location: Mapped[str | None] = mapped_column(String, nullable=True, default="footer")
   next_cue_display_location: Mapped[str | None] = mapped_column(String, nullable=True, default="header")
   header_font_family: Mapped[str | None] = mapped_column(String, nullable=True, default="Inter")
   header_color: Mapped[str | None] = mapped_column(String, nullable=True, default=None)
   footer_font_family: Mapped[str | None] = mapped_column(String, nullable=True, default="Inter")
   footer_color: Mapped[str | None] = mapped_column(String, nullable=True, default=None)
   
   # Theme and Styling
   theme_name: Mapped[str | None] = mapped_column(String, nullable=True, default="default")
   text_style: Mapped[str | None] = mapped_column(String, nullable=True, default="default")  # default, outline, shadow
   
   # Background Configuration
   background_type: Mapped[str | None] = mapped_column(String, nullable=True, default="color")  # image, color, transparent, preset
   background_color: Mapped[str | None] = mapped_column(String, nullable=True, default=None)
   background_image: Mapped[str | None] = mapped_column(String, nullable=True, default=None) # base64
   background_preset: Mapped[str | None] = mapped_column(String, nullable=True, default=None)  # corporate, parchment, crowd, etc.
   
   # Progress Bar Configuration
   progress_style: Mapped[str | None] = mapped_column(String, nullable=True, default="bottom_bar")  # bottom_bar, top_bar, ring, hidden
   progress_color_main: Mapped[str | None] = mapped_column(String, nullable=True, default=None)
   progress_color_secondary: Mapped[str | None] = mapped_column(String, nullable=True, default=None)
   progress_color_tertiary: Mapped[str | None] = mapped_column(String, nullable=True, default=None)
   
   # Timestamps
   created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
   updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
   deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
   is_deleted: Mapped[bool] = mapped_column(default=False, index=True)
   
   # Constraints
   __table_args__ = (
       UniqueConstraint('created_by_user_id', 'name', name='uq_user_display_name'),
   )
