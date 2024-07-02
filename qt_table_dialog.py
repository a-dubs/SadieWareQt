from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QLabel, QDialogButtonBox, QMessageBox
from db_managers import BaseManager
from db_setup import AREA_CODE_MANAGER, EQUIPMENT_MANAGER, DEVICE_TYPE_MANAGER, ValidationError

class BaseDialog(QDialog):
    def __init__(self, title: str, id: int = None, parent=None, fields: dict = None, manager: BaseManager = None, focused_field: str = None):
        super().__init__(parent=parent)
        self.setWindowTitle(title)
        self.id = id
        self.manager = manager
        self.fields = []
        self.focused_field = focused_field
        self.field_widgets = {}
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red")

        form_layout = QFormLayout()
        for label, value in fields.items():
            field_edit = QLineEdit(value)
            form_layout.addRow(QLabel(label + ":"), field_edit)
            self.fields.append(field_edit)
            self.field_widgets[label] = field_edit

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
        if self.focused_field and self.focused_field in self.field_widgets:
            self.field_widgets[self.focused_field].setFocus()
        elif self.fields:
            self.fields[0].setFocus()

    def get_data(self):
        """
        Get the data from the fields and return a dictionary of the data
        """
        data = {}
        for field, value in zip(self.manager.model._fields_map.values(), self.fields):
            data[field] = value.text()
        return data

    def on_accept(self):
        data = self.get_data()
        try:
            if self.id is None:
                new_object = self.manager.model(**data)
                self.manager.add(new_object)
            else:
                self.manager.update(self.id, data)
            self.accept()
        except ValidationError as e:
            self.error_label.setText(str(e))
        except Exception as e:
            self.error_label.setText("Unexpected error occurred")
            raise e


class AreaCodeDialog(BaseDialog):
    def __init__(self, title: str, id: int = None, parent=None, fields: dict = None, focused_field: str = None):
        super().__init__(id=id, title=title, parent=parent, fields=fields, manager=AREA_CODE_MANAGER, focused_field=focused_field)


class EquipmentDialog(BaseDialog):
    def __init__(self, title: str, id: int = None, parent=None, fields: dict = None, focused_field: str = None):
        super().__init__(id=id, title=title, parent=parent, fields=fields, manager=EQUIPMENT_MANAGER, focused_field=focused_field)


class DeviceTypeDialog(BaseDialog):
    def __init__(self, title: str, id: int = None, parent=None, fields: dict = None, focused_field: str = None):
        super().__init__(id=id, title=title, parent=parent, fields=fields, manager=DEVICE_TYPE_MANAGER, focused_field=focused_field)
