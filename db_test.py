from sqlalchemy.orm import Session

from db_classes import *
from db_managers import *
from db_setup import session

# Create managers
equipment_manager = EquipmentManager(session)
device_type_manager = DeviceTypeManager(session)
area_code_manager = AreaCodeManager(session)


# Function to delete existing records if they match the new records
def delete_existing_records():
    # Check and delete existing device type
    existing_device_type = device_type_manager.filter(lambda model: model.device_type == "PLC")
    for device_type in existing_device_type:
        device_type_manager.delete(device_type.id)

    # Check and delete existing area code
    existing_area_code = area_code_manager.filter(lambda model: model.area_code == "B2")
    for area_code in existing_area_code:
        area_code_manager.delete(area_code.id)

    # Check and delete existing equipment
    existing_equipment = equipment_manager.filter(lambda model: model.name == "EQ124")
    for equipment in existing_equipment:
        equipment_manager.delete(equipment.id)


# Call the function to delete existing records
delete_existing_records()

# Add new records
new_device_type = DeviceType(device_type="PLC", description="Programmable Logic Controller")
device_type_manager.add(new_device_type)

new_area_code = AreaCode(area_code="B2", description="Backup Area")
area_code_manager.add(new_area_code)

new_equipment = Equipment(
    name="EQ124",
    application="Conveyor Belt",
    device_type_id=new_device_type.id,
    area_code_id=new_area_code.id,
    specs_description="Conveyor belt for sorting system",
    manufacturer="Conveyor Inc",
    vendor="Machinery Suppliers",
)
equipment_manager.add(new_equipment)

# Query records
all_equipment = equipment_manager.get_all()
for equipment in all_equipment:
    print(equipment.name, equipment.application)

# Update a record
updated_equipment = equipment_manager.update(new_equipment.id, {"specs_description": "Updated specs description"})

# Delete a record
equipment_manager.delete(new_equipment.id)

# Use the filter method to get equipment with a specific application
filtered_equipment = equipment_manager.filter(lambda model: model.application == "Conveyor Belt")
for equipment in filtered_equipment:
    print(f"Filtered Equipment: {equipment.name}, Application: {equipment.application}")

# Use the filter method to get area codes that start with 'B'
filtered_area_codes = area_code_manager.filter(lambda model: model.area_code.startswith("B"))
for area_code in filtered_area_codes:
    print(f"Filtered Area Code: {area_code.area_code}, Description: {area_code.description}")
