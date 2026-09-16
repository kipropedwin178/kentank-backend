from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.jwt import create_access_token
from app.core.security import verify_password
from app.models.admin import AdminUser


def authenticate_admin(
    db: Session,
    phone_number: str,
    email: str,
    password: str,
) -> AdminUser:
    statement = select(AdminUser).where(
        AdminUser.phone_number == phone_number,
        AdminUser.email == email,
    )

    admin = db.execute(statement).scalar_one_or_none()

    if admin is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin credentials.",
        )

    if not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin account is inactive.",
        )

    if not verify_password(
        password,
        admin.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin credentials.",
        )

    return admin


def create_admin_access_token(admin: AdminUser) -> str:
    token_data = {
        "sub": str(admin.id),
        "role": "admin",
    }

    return create_access_token(token_data)