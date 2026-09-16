from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.auth import AdminLoginRequest
from app.services.auth_service import (
    authenticate_admin,
    create_admin_access_token,
)


router = APIRouter(
    prefix="/kentankd",
    tags=["Admin Authentication"],
)


@router.post("/login")
def admin_login(
    login_data: AdminLoginRequest,
    db: Session = Depends(get_db),
):
    admin = authenticate_admin(
        db=db,
        phone_number=login_data.phone_number,
        email=login_data.email,
        password=login_data.password,
    )

    access_token = create_admin_access_token(admin)

    return {
        "message": "Admin login successful.",
        "access_token": access_token,
        "token_type": "bearer",
    }