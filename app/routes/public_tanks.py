from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.models.tank import WaterTank
from app.models.tank_image import TankImage
from app.schemas.tank import TankResponse
from app.schemas.tank_image import TankImageResponse


router = APIRouter(
    prefix="/tanks",
    tags=["Public Tanks"],
)


# =========================================================
# GET ALL ACTIVE TANKS
# =========================================================

@router.get(
    "",
    response_model=list[TankResponse],
)
def get_public_tanks(
    db: Session = Depends(get_db),
):
    statement = (
        select(WaterTank)
        .where(
            WaterTank.is_active.is_(True)
        )
        .order_by(
            WaterTank.updated_at.desc()
        )
    )

    return list(
        db.execute(statement).scalars().all()
    )


# =========================================================
# GET ONE ACTIVE TANK
# =========================================================

@router.get(
    "/{tank_id}",
    response_model=TankResponse,
)
def get_public_tank(
    tank_id: int,
    db: Session = Depends(get_db),
):
    tank = db.get(
        WaterTank,
        tank_id,
    )

    if tank is None or not tank.is_active:
        from fastapi import HTTPException, status

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Water tank not found.",
        )

    return tank


# =========================================================
# GET TANK IMAGES
# =========================================================

@router.get(
    "/{tank_id}/images",
    response_model=list[TankImageResponse],
)
def get_public_tank_images(
    tank_id: int,
    db: Session = Depends(get_db),
):
    tank = db.get(
        WaterTank,
        tank_id,
    )

    if tank is None or not tank.is_active:
        return []

    statement = (
        select(TankImage)
        .where(
            TankImage.tank_id == tank_id
        )
        .order_by(
            TankImage.created_at.asc()
        )
    )

    return list(
        db.execute(statement).scalars().all()
    )