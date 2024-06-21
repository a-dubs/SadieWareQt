from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QDialog,
    QFormLayout,
    QDialogButtonBox,
)
from PySide6.QtCore import Qt

from db_classes import AreaCode
from db_setup import *

class BaseDialog(QDialog):
    def __init__(self, title: str, id: int = None, parent=None, fields: dict = None):
        """
        Base Class for Pop up dialogues that can both edit and create new entries for a table.

        :param id: The ID of the entry to edit. If None, then a new entry is being added.
        :param parent: The parent widget.
        """
        super().__init__(parent=parent)
        self.setWindowTitle("Details")
        self.windowTitle = f"Edit {title}" if id is not None else f"New {title}"
        self.id = id
        self.fields = []
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red")

        form_layout = QFormLayout()

        for label, value in fields.items():
            field_edit = QLineEdit(value)
            form_layout.addRow(QLabel(label + ":"), field_edit)
            self.fields.append(field_edit)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.on_accept)
        self.button_box.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(self.error_label)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def showEvent(self, event):
        super().showEvent(event)
        if self.fields:
            self.fields[0].setFocus()

    def get_data(self):
        """
        Get the form data from all fields.

        :return: A list of the text from each field.
        """
        return [field.text() for field in self.fields]

    def on_accept(self):
        if not self.validate():
            return
        self.accept()

    def validate(self):
        return True


class AreaCodeDialog(BaseDialog):

    def validate(self):
        area_code, description = self.get_data()
        existing_codes = AREA_CODE_MANAGER.filter(lambda model: model.area_code == area_code)
        if existing_codes:
            if len(existing_codes) > 1 or (self.id is not None and existing_codes[0].id != self.id):
                self.error_label.setText(f"Area code '{area_code}' already exists")
                return False
        if len(description.strip()) == 0:
            self.error_label.setText("Description cannot be empty")
            return False
        return True

    def on_accept(self):
        area_code, description = self.get_data()
        try:
            if not self.validate():
                return
            # if None, then we are not editing
            if self.id is None:
                new_area_code = AreaCode(area_code=area_code, description=description)
                AREA_CODE_MANAGER.add(new_area_code)
            # otherwise we are editing
            else:
                AREA_CODE_MANAGER.update(self.id, {"area_code": area_code, "description": description})
            self.accept()
        except Exception as e:
            self.error_label.setText("Unexpected error occurred")


class DeviceTypeDialog(BaseDialog):
    def validate(self):
        device_type, description = self.get_data()
        existing_codes = DEVICE_TYPE_MANAGER.filter(lambda model: model.device_type == device_type)
        if existing_codes:
            if len(existing_codes) > 1 or (self.id is not None and existing_codes[0].id != self.id):
                self.error_label.setText(f"Device type '{device_type}' already exists")
                return False
        if len(description.strip()) == 0:
            self.error_label.setText("Description cannot be empty")
            return False
        return True

    def on_accept(self):
        device_type, description = self.get_data()
        try:
            if not self.validate():
                return
            # if None, then we are not editing
            if self.id is None:
                new_device_type = DeviceType(device_type=device_type, description=description)
                DEVICE_TYPE_MANAGER.add(new_device_type)
            # otherwise we are editing
            else:
                DEVICE_TYPE_MANAGER.update(self.id, {"device_type": device_type, "description": description})
            self.accept()
        except Exception as e:
            self.error_label.setText("Unexpected error occurred")


class EquipmentDialog(BaseDialog):
    def validate(self):
        device_type, description = self.get_data()
        existing_codes = EQUIPMENT_MANAGER.filter(lambda model: model.device_type == device_type)
        if existing_codes:
            if len(existing_codes) > 1 or (self.id is not None and existing_codes[0].id != self.id):
                self.error_label.setText(f"Device type '{device_type}' already exists")
                return False
        if len(description.strip()) == 0:
            self.error_label.setText("Description cannot be empty")
            return False
        return True

    def on_accept(self):
        device_type, description = self.get_data()
        try:
            if not self.validate():
                return
            # if None, then we are not editing
            if self.id is None:
                new_device_type = Equipment(device_type=device_type, description=description)
                EQUIPMENT_MANAGER.add(new_device_type)
            # otherwise we are editing
            else:
                EQUIPMENT_MANAGER.update(self.id, {"device_type": device_type, "description": description})
            self.accept()
        except Exception as e:
            self.error_label.setText("Unexpected error occurred")
