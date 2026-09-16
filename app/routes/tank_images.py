from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin, get_db
from app.models.admin import AdminUser
from app.schemas.tank_image import TankImageResponse
from app.services.tank_image_service import (
    create_tank_image,
    delete_tank_image,
    get_tank_image,
    get_tank_images,
)
from app.utils.image_upload import save_tank_image


router = APIRouter(
    prefix="/kentankd/tanks",
    tags=["Admin Tank Images"],
)


@router.post(
    "/{tank_id}/images/upload",
    response_model=TankImageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_tank_image_endpoint(
    tank_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin),
):
    image_url, cloudinary_public_id = await save_tank_image(
        file
    )

    return create_tank_image(
        db=db,
        tank_id=tank_id,
        image_url=image_url,
        cloudinary_public_id=cloudinary_public_id,
    )


@router.get(
    "/{tank_id}/images",
    response_model=list[TankImageResponse],
)
def list_tank_images_endpoint(
    tank_id: int,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin),
):
    return get_tank_images(
        db=db,
        tank_id=tank_id,
    )


@router.get(
    "/images/{image_id}",
    response_model=TankImageResponse,
)
def get_tank_image_endpoint(
    image_id: int,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin),
):
    return get_tank_image(
        db=db,
        image_id=image_id,
    )


@router.delete(
    "/images/{image_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_tank_image_endpoint(
    image_id: int,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin),
):
    delete_tank_image(
        db=db,
        image_id=image_id,
    )