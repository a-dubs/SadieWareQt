from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QTableWidget,
    QTableWidgetItem,
    QDialog,
    QFormLayout,
    QDialogButtonBox,
    QPushButton,
    QHBoxLayout,
    QMessageBox,
    QComboBox,
)
from PySide6.QtCore import Qt

from db_setup import session
from db_managers import *

area_code_manager = AreaCodeManager(session)

class AreaCodeTable(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Area Codes")
        self.setGeometry(300, 100, 800, 600)

        # Create and connect table
        self.table_widget = QTableWidget()
        self.table_widget.setSortingEnabled(True)
        self.table_widget.horizontalHeader().setSectionsClickable(True)
        self.table_widget.horizontalHeader().sectionClicked.connect(self.sort_table)
        self.table_widget.itemSelectionChanged.connect(self.update_button_states)
        self.table_widget.cellDoubleClicked.connect(self.edit_entry)
        
        self.load_data()

        # Create search bar and column selector
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.textChanged.connect(self.filter_table)

        self.column_selector = QComboBox()
        self.column_selector.addItems(["All Columns", "Area Code", "Description"])
        self.column_selector.currentIndexChanged.connect(self.filter_table)

        self.search_layout = QHBoxLayout()
        self.search_layout.addWidget(QLabel("Search:"))
        self.search_layout.addWidget(self.search_bar)
        self.search_layout.addWidget(QLabel("In Column:"))
        self.search_layout.addWidget(self.column_selector)

        # Create and connect buttons
        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self.edit_entry)
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_entry)
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_entry)
        self.duplicate_button = QPushButton("Duplicate")
        self.duplicate_button.clicked.connect(self.duplicate_entry)

        # Disable the edit, delete, and duplicate buttons initially
        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)
        self.duplicate_button.setEnabled(False)

        # Style buttons
        self.style_buttons()

        # Create button layout
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.duplicate_button)
        button_layout.addStretch()

        # Create main layout
        layout = QVBoxLayout()
        layout.addLayout(self.search_layout)
        layout.addWidget(self.table_widget)
        layout.addLayout(button_layout)

        # Create main container widget
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def style_buttons(self):
        button_style = """
        QPushButton {
            min-width: 80px;
            max-width: 100px;
            min-height: 30px;
            max-height: 40px;
            padding: 6px;
            border: 2px solid #5F6368;
            border-radius: 5px;
            background-color: #F1F3F4;
            color: #202124;
        }
        QPushButton:hover {
            background-color: #E8EAED;
            border-color: #202124;
        }
        QPushButton:pressed {
            background-color: #D2D6DB;
        }
        QPushButton:disabled {
            background-color: #E0E0E0;
            color: #9E9E9E;
        }
        """
        self.edit_button.setStyleSheet(button_style)
        self.add_button.setStyleSheet(button_style)
        self.delete_button.setStyleSheet(button_style)
        self.duplicate_button.setStyleSheet(button_style)

    def load_data(self):
        self.table_widget.blockSignals(True)
        area_codes = area_code_manager.get_all()
        self.table_widget.setRowCount(len(area_codes))
        self.table_widget.setColumnCount(3)  # Include the ID column
        self.table_widget.setHorizontalHeaderLabels(["ID", "Area Code", "Description"])

        for row, area_code in enumerate(area_codes):
            id_item = QTableWidgetItem(str(area_code.id))
            id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table_widget.setItem(row, 0, id_item)

            area_code_item = QTableWidgetItem(area_code.area_code)
            area_code_item.setFlags(area_code_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table_widget.setItem(row, 1, area_code_item)

            description_item = QTableWidgetItem(area_code.description)
            description_item.setFlags(description_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table_widget.setItem(row, 2, description_item)

        self.table_widget.setColumnHidden(0, True)  # Hide the ID column
        self.table_widget.blockSignals(False)

    def sort_table(self, index):
        self.table_widget.sortItems(index, Qt.AscendingOrder if self.table_widget.horizontalHeader().sortIndicatorOrder() == Qt.AscendingOrder else Qt.DescendingOrder)

    def filter_table(self):
        filter_text = self.search_bar.text().strip().lower()
        column = self.column_selector.currentIndex()
        
        for i in range(self.table_widget.rowCount()):
            item_code = self.table_widget.item(i, 1)
            item_desc = self.table_widget.item(i, 2)
            if column == 0:  # All Columns
                if filter_text in item_code.text().strip().lower() or filter_text in item_desc.text().strip().lower():
                    self.table_widget.showRow(i)
                else:
                    self.table_widget.hideRow(i)
            elif column == 1:  # Area Code
                if filter_text in item_code.text().strip().lower():
                    self.table_widget.showRow(i)
                else:
                    self.table_widget.hideRow(i)
            elif column == 2:  # Description
                if filter_text in item_desc.text().strip().lower():
                    self.table_widget.showRow(i)
                else:
                    self.table_widget.hideRow(i)

    def edit_entry(self, row=None, column=None):
        if row is None:
            selected_row = self.table_widget.currentRow()
        else:
            selected_row = row

        if selected_row < 0:
            QMessageBox.warning(self, "No selection", "Please select a row to edit")
            return

        id_item = self.table_widget.item(selected_row, 0)
        area_code_item = self.table_widget.item(selected_row, 1)
        description_item = self.table_widget.item(selected_row, 2)

        dialog = AreaCodeDialog(
            id=int(id_item.text()),
            parent=self,
            area_code=area_code_item.text(),
            description=description_item.text(),
        )
        if dialog.exec():
            self.load_data()

    def add_entry(self):
        dialog = AreaCodeDialog(parent=self)
        if dialog.exec():
            self.load_data()

    def delete_entry(self):
        selected_row = self.table_widget.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "No selection", "Please select a row to delete")
            return

        response = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this entry?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if response == QMessageBox.StandardButton.Yes:
            id_item = self.table_widget.item(selected_row, 0)
            area_code_id = int(id_item.text())
            area_code_manager.delete(area_code_id)
            self.load_data()

    def duplicate_entry(self):
        selected_row = self.table_widget.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "No selection", "Please select a row to duplicate")
            return

        id_item = self.table_widget.item(selected_row, 0)
        area_code_item = self.table_widget.item(selected_row, 1)
        description_item = self.table_widget.item(selected_row, 2)

        dialog = AreaCodeDialog(
            id=None,  # New entry
            parent=self,
            area_code=area_code_item.text(),
            description=description_item.text(),
        )
        if dialog.exec():
            self.load_data()

    def update_button_states(self):
        has_selection = bool(self.table_widget.selectedItems())
        self.edit_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)
        self.duplicate_button.setEnabled(has_selection)


class BaseDialog(QDialog):
    def __init__(self, id: int = None, parent=None, fields: dict = None):
        """
        Base Class for Pop up dialogues that can both edit and create new entries for a table.

        :param id: The ID of the entry to edit. If None, then a new entry is being added.
        :param parent: The parent widget.
        """
        super().__init__(parent=parent)
        self.setWindowTitle("Details")
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
    def __init__(self, id: int = None, parent=None, area_code="", description=""):
        """
        Pop up dialogue for either adding or editing an area code.

        :param id: The ID of the area code to edit. If None, then a new area code is being added.
        :param parent: The parent widget.
        :param area_code: The area code that the dialog text field will be initialized with.
        :param description: The description that the dialog text field will be initialized with.
        """
        fields = {"Area Code": area_code, "Description": description}
        self.windowTitle = "Edit Area Code" if id is not None else "Add Area Code"
        super().__init__(
            id=id,
            parent=parent,
            fields=fields,
        )

    def validate(self):
        area_code, description = self.get_data()
        existing_codes = area_code_manager.filter(lambda model: model.area_code == area_code)
        if existing_codes:
            if len(existing_codes) > 1 or (self.id is not None and existing_codes[0].id != self.id):
                self.error_label.setText("Area code already exists")
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
                area_code_manager.add(new_area_code)
            # otherwise we are editing
            else:
                area_code_manager.update(self.id, {"area_code": area_code, "description": description})
            self.accept()
        except Exception as e:
            self.error_label.setText("Unexpected error occurred")


if __name__ == "__main__":
    # Create the Qt Application
    app = QApplication([])

    # Create and show the form
    window = AreaCodeTable()
    window.show()

    # Run the main Qt loop
    app.exec()
