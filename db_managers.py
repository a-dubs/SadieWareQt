from typing import Any, Dict
from sqlalchemy.orm import Session
from db_classes import *

class ValidationError(Exception):
    pass

class BaseManager:
    def __init__(self, session: Session, model: BaseBase):
        self.session = session
        self.model = model

    def validate(self, obj):
        # Check for unique constraints
        unique_fields = get_unique_fields(self.model)
        self.check_uniqueness(obj, unique_fields)

        # Check for nullable constraints
        nullable_fields = get_nullable_fields(self.model)
        self.check_nullables(obj, nullable_fields)

    def check_uniqueness(self, obj, unique_fields: Dict[str, str]):
        """
        Checks for uniqueness constraints on the model's fields.

        Args:
            obj (BaseBase): The object to validate.
            unique_fields (Dict[str, str]): A dictionary of field names to error messages.

        Raises:
            ValidationError: If a uniqueness constraint is violated.
        """
        with self.session.no_autoflush:
            for field, message in unique_fields.items():
                field_value = getattr(obj, field)
                if obj.id:
                    existing = self.session.query(self.model).filter(
                        getattr(self.model, field) == field_value, 
                        self.model.id != obj.id
                    ).first()
                else:
                    existing = self.session.query(self.model).filter(
                        getattr(self.model, field) == field_value
                    ).first()
                
                if existing:
                    raise ValidationError(message.format(value=field_value))

    def check_nullables(self, obj, nullable_fields: Dict[str, str]):
        """
        Checks for non-nullable constraints on the model's fields.

        Args:
            obj (BaseBase): The object to validate.
            nullable_fields (Dict[str, str]): A dictionary of field names to error messages.

        Raises:
            ValidationError: If a non-nullable constraint is violated.
        """
        for field, message in nullable_fields.items():
            field_value = getattr(obj, field)
            if field_value is None or (isinstance(field_value, str) and not field_value.strip()):
                raise ValidationError(message)

    def add(self, obj):
        self.validate(obj)
        self.session.add(obj)
        self.session.commit()
        return obj

    def get(self, obj_id):
        return self.session.query(self.model).get(obj_id)

    def get_all(self):
        return self.session.query(self.model).all()

    def update(self, obj_id, updates: dict):
        print("updates dict:", updates)
        obj = self.session.query(self.model).get(obj_id)
        if obj:
            for key, value in updates.items():
                if key in self.model._fields_map:
                    field_name = self.model._fields_map.get(key)
                else:
                    field_name = key
                if getattr(obj, field_name) == value:
                    continue
                print(f"updating {field_name} to {value}")
                setattr(obj, field_name, value)
            self.validate(obj)
            self.session.commit()
        return obj

    def delete(self, obj_id):
        obj = self.session.query(self.model).get(obj_id)
        if obj:
            self.session.delete(obj)
            self.session.commit()
        return obj

    def filter(self, filter_func):
        return self.session.query(self.model).filter(filter_func(self.model)).all()

    def create_pairs_for_table(self) -> list[tuple[str, Any]]:
        # first get all all data
        data = self.get_all()
        # get the fields
        fields = self.model._fields
        # create the pairs by iterating through the fields and using getattr to get the value
        rows = []
        for entry in data:
            rows.append([(field, getattr(entry, field)) for field in fields])
        return rows

def get_unique_fields(model):
    """
    Returns a dictionary mapping unique field names to their validation error messages.

    Args:
        model (BaseBase): The SQLAlchemy model class.

    Returns:
        Dict[str, str]: A dictionary mapping field names to error messages.
    """
    unique_fields = {}
    for field_name, column in model.__table__.columns.items():
        if column.unique:
            human_readable_name = None
            for human_readable, mapped_field in model._fields_map.items():
                if mapped_field == field_name:
                    human_readable_name = human_readable
                    break
            if human_readable_name:
                unique_fields[field_name] = f"{human_readable_name} with value '{{value}}' already exists."
    return unique_fields

def get_nullable_fields(model):
    """
    Returns a dictionary mapping non-nullable field names to their validation error messages.

    Args:
        model (BaseBase): The SQLAlchemy model class.

    Returns:
        Dict[str, str]: A dictionary mapping field names to error messages.
    """
    nullable_fields = {}
    for field_name, column in model.__table__.columns.items():
        if not column.nullable:
            human_readable_name = None
            for human_readable, mapped_field in model._fields_map.items():
                if mapped_field == field_name:
                    human_readable_name = human_readable
                    break
            if human_readable_name:
                nullable_fields[field_name] = f"{human_readable_name} is required."
    return nullable_fields

class EquipmentManager(BaseManager):
    def __init__(self, session: Session):
        super().__init__(session, Equipment)

class DeviceTypeManager(BaseManager):
    def __init__(self, session: Session):
        super().__init__(session, DeviceType)

class AreaCodeManager(BaseManager):
    def __init__(self, session: Session):
        super().__init__(session, AreaCode)
