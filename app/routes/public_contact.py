from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.contact import ContactInformationResponse
from app.services.contact_service import get_contact_information


router = APIRouter(
    prefix="/contact",
    tags=["Public Contact"],
)


@router.get(
    "",
    response_model=ContactInformationResponse,
)
def get_public_contact_endpoint(
    db: Session = Depends(get_db),
):
    contact = get_contact_information(db)

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact information is not available.",
        )

    return contact