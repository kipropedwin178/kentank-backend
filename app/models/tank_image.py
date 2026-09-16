from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class TankImage(Base):
    __tablename__ = "tank_images"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    tank_id: Mapped[int] = mapped_column(
        ForeignKey("water_tanks.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    image_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    cloudinary_public_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )