from pathlib import Path

import cloudinary.uploader
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core import cloudinary as cloudinary_config
from app.models.tank import WaterTank
from app.models.tank_image import TankImage


def create_tank_image(
    db: Session,
    tank_id: int,
    image_url: str,
    cloudinary_public_id: str | None = None,
) -> TankImage:
    tank = db.get(WaterTank, tank_id)

    if tank is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Water tank not found.",
        )

    image = TankImage(
        tank_id=tank_id,
        image_url=image_url,
        cloudinary_public_id=cloudinary_public_id,
    )

    db.add(image)

    try:
        db.commit()
        db.refresh(image)

    except Exception:
        db.rollback()

        # If the image was already uploaded to Cloudinary
        # but the database operation failed, remove the
        # Cloudinary image to prevent an orphaned file.
        if cloudinary_public_id:
            try:
                cloudinary.uploader.destroy(
                    cloudinary_public_id,
                    resource_type="image",
                )
            except Exception:
                pass

        raise

    return image


def get_tank_images(
    db: Session,
    tank_id: int,
) -> list[TankImage]:
    tank = db.get(WaterTank, tank_id)

    if tank is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Water tank not found.",
        )

    statement = (
        select(TankImage)
        .where(TankImage.tank_id == tank_id)
        .order_by(TankImage.created_at.asc())
    )

    return list(
        db.execute(statement).scalars().all()
    )


def get_tank_image(
    db: Session,
    image_id: int,
) -> TankImage:
    image = db.get(TankImage, image_id)

    if image is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tank image not found.",
        )

    return image


def delete_tank_image(
    db: Session,
    image_id: int,
) -> None:
    image = get_tank_image(
        db=db,
        image_id=image_id,
    )

    # New images stored on Cloudinary
    if image.cloudinary_public_id:
        try:
            result = cloudinary.uploader.destroy(
                image.cloudinary_public_id,
                resource_type="image",
            )

            if result.get("result") not in {"ok", "not found"}:
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="Unable to delete image from Cloudinary.",
                )

        except HTTPException:
            raise

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Unable to delete image from Cloudinary.",
            )

    # Legacy images stored locally
    else:
        image_url = image.image_url

        if image_url.startswith("/uploads/"):
            file_path = Path(image_url.lstrip("/"))

            if file_path.is_file():
                file_path.unlink()

    db.delete(image)
    db.commit()