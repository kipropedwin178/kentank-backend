from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ContactInformationBase(BaseModel):
    call_number: str = Field(
        min_length=7,
        max_length=20,
    )

    whatsapp_number: str = Field(
        min_length=7,
        max_length=20,
    )

    email: EmailStr

    physical_address: str | None = Field(
        default=None,
        max_length=500,
    )

    business_hours: str = Field(
        min_length=2,
        max_length=255,
    )


class ContactInformationCreate(ContactInformationBase):
    pass


class ContactInformationUpdate(BaseModel):
    call_number: str | None = Field(
        default=None,
        min_length=7,
        max_length=20,
    )

    whatsapp_number: str | None = Field(
        default=None,
        min_length=7,
        max_length=20,
    )

    email: EmailStr | None = None

    physical_address: str | None = Field(
        default=None,
        max_length=500,
    )

    business_hours: str | None = Field(
        default=None,
        min_length=2,
        max_length=255,
    )


class ContactInformationResponse(ContactInformationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )