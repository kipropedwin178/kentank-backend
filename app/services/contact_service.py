from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.contact_info import ContactInformation
from app.schemas.contact import (
    ContactInformationCreate,
    ContactInformationUpdate,
)


def get_contact_information(
    db: Session,
) -> ContactInformation | None:
    statement = select(ContactInformation).order_by(
        ContactInformation.id.asc()
    )

    return db.execute(statement).scalars().first()


def create_contact_information(
    db: Session,
    contact_data: ContactInformationCreate,
) -> ContactInformation:
    existing_contact = get_contact_information(db)

    if existing_contact is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Contact information already exists. Update the existing information instead.",
        )

    contact = ContactInformation(
        call_number=contact_data.call_number,
        whatsapp_number=contact_data.whatsapp_number,
        email=contact_data.email,
        physical_address=contact_data.physical_address,
        business_hours=contact_data.business_hours,
    )

    db.add(contact)
    db.commit()
    db.refresh(contact)

    return contact


def update_contact_information(
    db: Session,
    contact_data: ContactInformationUpdate,
) -> ContactInformation:
    contact = get_contact_information(db)

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact information has not been configured yet.",
        )

    update_data = contact_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(contact, field, value)

    db.commit()
    db.refresh(contact)

    return contact