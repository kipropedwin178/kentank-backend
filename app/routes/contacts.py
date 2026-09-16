from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin, get_db
from app.models.admin import AdminUser
from app.schemas.contact import (
    ContactInformationCreate,
    ContactInformationResponse,
    ContactInformationUpdate,
)
from app.services.contact_service import (
    create_contact_information,
    get_contact_information,
    update_contact_information,
)


router = APIRouter(
    prefix="/kentankd/contacts",
    tags=["Admin Contact Information"],
)


@router.post(
    "",
    response_model=ContactInformationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_contact_endpoint(
    contact_data: ContactInformationCreate,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin),
):
    return create_contact_information(
        db=db,
        contact_data=contact_data,
    )


@router.get(
    "",
    response_model=ContactInformationResponse,
)
def get_contact_endpoint(
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin),
):
    contact = get_contact_information(db)

    if contact is None:
        return None

    return contact


@router.put(
    "",
    response_model=ContactInformationResponse,
)
def update_contact_endpoint(
    contact_data: ContactInformationUpdate,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin),
):
    return update_contact_information(
        db=db,
        contact_data=contact_data,
    )