from typing import Any
from sqlalchemy.orm import Session
from db_classes import *


class BaseManager:
    def __init__(self, session: Session, model: BaseBase):
        self.session = session
        self.model = model

    def add(self, obj):
        self.session.add(obj)
        self.session.commit()
        return obj

    def get(self, obj_id):
        return self.session.query(self.model).get(obj_id)

    def get_all(self):
        return self.session.query(self.model).all()

    def update(self, obj_id, updates: dict):
        obj = self.session.query(self.model).get(obj_id)
        if obj:
            for key, value in updates.items():
                setattr(obj, key, value)
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

    def create_pairs_for_table(self) -> list[tuple[str,Any]]:
        # first get all all data
        data = self.get_all()
        # get the fields
        fields = self.model._fields
        # create the pairs by iterating through the fields and using getattr to get the value
        rows = []
        for entry in data:
            rows.append([(field, getattr(entry, field)) for field in fields])
        return rows


class EquipmentManager(BaseManager):
    def __init__(self, session: Session):
        super().__init__(session, Equipment)


class DeviceTypeManager(BaseManager):
    def __init__(self, session: Session):
        super().__init__(session, DeviceType)


class AreaCodeManager(BaseManager):
    def __init__(self, session: Session):
        super().__init__(session, AreaCode)
