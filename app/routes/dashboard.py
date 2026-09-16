from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin, get_db
from app.models.admin import AdminUser
from app.models.contact_info import ContactInformation
from app.models.tank import WaterTank
from app.models.tank_image import TankImage


router = APIRouter(
    prefix="/kentankd/dashboard",
    tags=["Admin Dashboard"],
)


@router.get("")
def get_dashboard_statistics(
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin),
):
    total_tanks = db.scalar(
        select(func.count(WaterTank.id))
    ) or 0

    active_tanks = db.scalar(
        select(func.count(WaterTank.id)).where(
            WaterTank.is_active.is_(True)
        )
    ) or 0

    inactive_tanks = db.scalar(
        select(func.count(WaterTank.id)).where(
            WaterTank.is_active.is_(False)
        )
    ) or 0

    in_stock = db.scalar(
        select(func.count(WaterTank.id)).where(
            WaterTank.availability == "In Stock",
            WaterTank.is_active.is_(True),
        )
    ) or 0

    out_of_stock = db.scalar(
        select(func.count(WaterTank.id)).where(
            WaterTank.availability == "Out of Stock",
            WaterTank.is_active.is_(True),
        )
    ) or 0

    limited_stock = db.scalar(
        select(func.count(WaterTank.id)).where(
            WaterTank.availability == "Limited Stock",
            WaterTank.is_active.is_(True),
        )
    ) or 0

    total_images = db.scalar(
        select(func.count(TankImage.id))
    ) or 0

    contact_count = db.scalar(
        select(func.count(ContactInformation.id))
    ) or 0

    contact_configured = contact_count > 0

    return {
        "total_tanks": total_tanks,
        "active_tanks": active_tanks,
        "inactive_tanks": inactive_tanks,
        "availability": {
            "in_stock": in_stock,
            "out_of_stock": out_of_stock,
            "limited_stock": limited_stock,
        },
        "total_images": total_images,
        "contact_configured": contact_configured,
    }