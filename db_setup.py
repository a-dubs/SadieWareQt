from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_managers import AreaCodeManager, EquipmentManager, DeviceTypeManager

from db_classes import *
from db_managers import *

# Create the database engine
engine = create_engine("postgresql+psycopg2://postgres:letmein@localhost:5555/dev_sadieware_db")

# Create the tables
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

AREA_CODE_MANAGER = AreaCodeManager(session=session)
EQUIPMENT_MANAGER = EquipmentManager(session=session)
DEVICE_TYPE_MANAGER = DeviceTypeManager(session=session)