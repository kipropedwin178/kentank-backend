from pydantic import BaseModel, EmailStr, Field


class AdminLoginRequest(BaseModel):
    phone_number: str = Field(
        min_length=7,
        max_length=20,
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
    )