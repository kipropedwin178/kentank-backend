from datetime import datetime, timezone

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class ContactInformation(Base):
    __tablename__ = "contact_information"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    call_number: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    whatsapp_number: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    physical_address: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    business_hours: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )