from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Define the base class
Base = declarative_base()

class BaseBase(Base):
    __abstract__ = True
    _fields: list[str] = []

# Define the DeviceType class
class DeviceType(BaseBase):
    __tablename__ = "device_types"
    _fields = [
        "id",
        "device_type",
        "description",
    ]

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_type = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)

    # Relationship to Equipment
    equipments = relationship("Equipment", back_populates="device_type")


# Define the AreaCode class
class AreaCode(BaseBase):
    __tablename__ = "area_codes"
    _fields = [
        "id",
        "area_code",
        "description",
    ]

    id = Column(Integer, primary_key=True, autoincrement=True)
    area_code = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)

    # Relationship to Equipment
    equipments = relationship("Equipment", back_populates="area_code")


# Define the Equipment class
class Equipment(BaseBase):
    __tablename__ = "equipments"
    _fields = [
        "id",
        "name",
        "application",
        "device_type_id",
        "area_code_id",
        "specs_description",
        "manufacturer",
        "vendor",
    ]

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    application = Column(String, unique=True, nullable=False)
    device_type_id = Column(Integer, ForeignKey("device_types.id"), nullable=False)
    area_code_id = Column(Integer, ForeignKey("area_codes.id"), nullable=True)
    specs_description = Column(String, nullable=True)
    manufacturer = Column(String, nullable=True)
    vendor = Column(String, nullable=True)

    # Relationships
    device_type = relationship("DeviceType", back_populates="equipments")
    area_code = relationship("AreaCode", back_populates="equipments")
