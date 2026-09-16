from fastapi import HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.admin import AdminUser


def create_admin(
    db: Session,
    phone_number: str,
    email: str,
    password: str,
) -> AdminUser:
    existing_admin = db.execute(
        select(AdminUser).where(
            or_(
                AdminUser.phone_number == phone_number,
                AdminUser.email == email,
            )
        )
    ).scalar_one_or_none()

    if existing_admin:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An admin with this phone number or email already exists.",
        )

    admin = AdminUser(
        phone_number=phone_number,
        email=email,
        password_hash=hash_password(password),
        is_active=True,
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    return admin