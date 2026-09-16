from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


AvailabilityStatus = Literal[
    "In Stock",
    "Out of Stock",
    "Limited Stock",
]


class TankBase(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=255,
    )

    price: Decimal = Field(
        gt=0,
        max_digits=12,
        decimal_places=2,
    )

    description: str | None = Field(
        default=None,
        max_length=5000,
    )

    capacity_liters: int = Field(
        gt=0,
    )

    availability: AvailabilityStatus = "In Stock"

    is_active: bool = True


class TankCreate(TankBase):
    pass


class TankUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=255,
    )

    price: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=12,
        decimal_places=2,
    )

    description: str | None = Field(
        default=None,
        max_length=5000,
    )

    capacity_liters: int | None = Field(
        default=None,
        gt=0,
    )

    availability: AvailabilityStatus | None = None

    is_active: bool | None = None


class TankResponse(TankBase):
    id: int
    created_at: object
    updated_at: object

    model_config = ConfigDict(
        from_attributes=True,
    )