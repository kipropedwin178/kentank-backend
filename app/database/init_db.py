from app.database.base import Base
from app.database.session import engine

# Import models here
from app.models.admin import AdminUser
from app.models.tank import WaterTank
from app.models.tank_image import TankImage
from app.models.contact_info import ContactInformation


def init_db():
    Base.metadata.create_all(bind=engine)