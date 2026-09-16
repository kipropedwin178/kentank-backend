from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.tank import WaterTank
from app.schemas.tank import TankCreate, TankUpdate


def create_tank(
    db: Session,
    tank_data: TankCreate,
) -> WaterTank:
    tank = WaterTank(
        name=tank_data.name,
        price=tank_data.price,
        description=tank_data.description,
        capacity_liters=tank_data.capacity_liters,
        availability=tank_data.availability,
        is_active=tank_data.is_active,
    )

    db.add(tank)
    db.commit()
    db.refresh(tank)

    return tank


def get_tank(
    db: Session,
    tank_id: int,
) -> WaterTank:
    tank = db.get(WaterTank, tank_id)

    if tank is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Water tank not found.",
        )

    return tank


def get_tanks(
    db: Session,
    include_inactive: bool = False,
) -> list[WaterTank]:
    statement = select(WaterTank).order_by(
        WaterTank.created_at.desc()
    )

    if not include_inactive:
        statement = statement.where(
            WaterTank.is_active.is_(True)
        )

    return list(
        db.execute(statement).scalars().all()
    )


def update_tank(
    db: Session,
    tank_id: int,
    tank_data: TankUpdate,
) -> WaterTank:
    tank = get_tank(db, tank_id)

    update_data = tank_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(tank, field, value)

    db.commit()
    db.refresh(tank)

    return tank


def delete_tank(
    db: Session,
    tank_id: int,
) -> None:
    tank = get_tank(db, tank_id)

    db.delete(tank)
    db.commit()