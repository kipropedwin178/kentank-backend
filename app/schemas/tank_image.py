from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TankImageResponse(BaseModel):
    id: int
    tank_id: int
    image_url: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )