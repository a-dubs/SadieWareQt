from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Define the base class
Base = declarative_base()


# Define the DeviceType class
class DeviceType(Base):
    __tablename__ = "device_types"

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_type = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)

    # Relationship to Equipment
    equipments = relationship("Equipment", back_populates="device_type")


# Define the AreaCode class
class AreaCode(Base):
    __tablename__ = "area_codes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    area_code = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)

    # Relationship to Equipment
    equipments = relationship("Equipment", back_populates="area_code")


# Define the Equipment class
class Equipment(Base):
    __tablename__ = "equipments"

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
