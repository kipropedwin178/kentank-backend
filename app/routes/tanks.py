from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin, get_db
from app.models.admin import AdminUser
from app.schemas.tank import TankCreate, TankResponse, TankUpdate
from app.services.tank_service import (
    create_tank,
    delete_tank,
    get_tank,
    get_tanks,
    update_tank,
)


router = APIRouter(
    prefix="/kentankd/tanks",
    tags=["Admin Tanks"],
)


@router.post(
    "",
    response_model=TankResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_tank_endpoint(
    tank_data: TankCreate,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin),
):
    return create_tank(
        db=db,
        tank_data=tank_data,
    )


@router.get(
    "",
    response_model=list[TankResponse],
)
def list_tanks_endpoint(
    include_inactive: bool = Query(
        default=False,
        description="Include inactive tanks in the results.",
    ),
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin),
):
    return get_tanks(
        db=db,
        include_inactive=include_inactive,
    )


@router.get(
    "/{tank_id}",
    response_model=TankResponse,
)
def get_tank_endpoint(
    tank_id: int,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin),
):
    return get_tank(
        db=db,
        tank_id=tank_id,
    )


@router.put(
    "/{tank_id}",
    response_model=TankResponse,
)
def update_tank_endpoint(
    tank_id: int,
    tank_data: TankUpdate,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin),
):
    return update_tank(
        db=db,
        tank_id=tank_id,
        tank_data=tank_data,
    )


@router.delete(
    "/{tank_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_tank_endpoint(
    tank_id: int,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin),
):
    delete_tank(
        db=db,
        tank_id=tank_id,
    )