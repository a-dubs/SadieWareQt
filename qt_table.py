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
from db_setup import *
from qt_table_dialog import *


class SimpleTable(QWidget):
    def __init__(self, manager, title, columns, dialog_class: BaseDialog):
        super().__init__()
        self.manager = manager
        self.title = title
        self.columns = columns
        self.dialog_class = dialog_class

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        
        # Create table widget
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
        self.column_selector.addItems(["All Columns"] + self.columns[1:])
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

        self.setLayout(layout)

    def style_buttons(self):
        button_style = """
        QPushButton {
            min-width: 60px;
            max-width: 100px;
            min-height: 20px;
            max-height: 30px;
            padding: 6px;
            border: 1px solid #5F6368;
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
        prepared_rows_of_field_value_pairs = self.manager.create_pairs_for_table()
        if len(prepared_rows_of_field_value_pairs) == 0:
            self.table_widget.setRowCount(0)
            self.table_widget.setColumnCount(0)
            self.table_widget.setHorizontalHeaderLabels([])
            self.table_widget.blockSignals(False)
            return
        
        self.table_widget.setRowCount(len(prepared_rows_of_field_value_pairs))
        self.table_widget.setColumnCount(len(prepared_rows_of_field_value_pairs[0]))
        self.table_widget.setHorizontalHeaderLabels([pair[0] for pair in prepared_rows_of_field_value_pairs[0]])

        for row_no, field_value_pairs in enumerate(prepared_rows_of_field_value_pairs):
            for col_no, pair in enumerate(field_value_pairs):
                cell = QTableWidgetItem(str(pair[1]))
                cell.setFlags(cell.flags() & ~Qt.ItemIsEditable)
                self.table_widget.setItem(row_no, col_no, cell)

        self.table_widget.setColumnHidden(0, True)  # Hide the ID column
        self.table_widget.blockSignals(False)

    def sort_table(self, index):
        self.table_widget.sortItems(index, Qt.AscendingOrder if self.table_widget.horizontalHeader().sortIndicatorOrder() == Qt.AscendingOrder else Qt.DescendingOrder)

    def filter_table(self):
        filter_text = self.search_bar.text().strip().lower()
        column = self.column_selector.currentIndex()  # This will give the index relative to the combo box

        for i in range(self.table_widget.rowCount()):
            row_matches = False
            for col in range(1, self.table_widget.columnCount()):
                item = self.table_widget.item(i, col)
                if column == 0:  # All Columns
                    if filter_text in item.text().strip().lower():
                        row_matches = True
                        break
                elif col == column:  # Specific Column
                    if filter_text in item.text().strip().lower():
                        row_matches = True
                        break
            if row_matches:
                self.table_widget.showRow(i)
            else:
                self.table_widget.hideRow(i)

    def edit_entry(self):
        selected_row = self.table_widget.currentRow()

        if selected_row < 0:
            QMessageBox.warning(self, "No selection", "Please select a row to edit")
            return

        id_item = self.table_widget.item(selected_row, 0)
        fields = {self.columns[col]: self.table_widget.item(selected_row, col).text() for col in range(1, self.table_widget.columnCount())}

        dialog = self.dialog_class(
            title=self.title,
            id=int(id_item.text()),
            parent=self,
            fields=fields,
        )
        if dialog.exec():
            self.load_data()

    def add_entry(self):
        dialog = self.dialog_class(title=self.title, parent=self, fields={col: "" for col in self.columns[1:]},)
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
            obj_id = int(id_item.text())
            self.manager.delete(obj_id)
            self.load_data()

    def duplicate_entry(self):
        selected_row = self.table_widget.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "No selection", "Please select a row to duplicate")
            return

        id_item = self.table_widget.item(selected_row, 0)
        fields = {self.columns[col]: self.table_widget.item(selected_row, col).text() for col in range(1, self.table_widget.columnCount())}


        dialog = self.dialog_class(
            title=self.title,
            id=None,  # New entry
            parent=self,
            fields=fields,
        )
        if dialog.exec():
            self.load_data()

    def update_button_states(self):
        has_selection = bool(self.table_widget.selectedItems())
        self.edit_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)
        self.duplicate_button.setEnabled(has_selection)


class AreaCodeTable(SimpleTable):
    def __init__(self):
        columns = ["ID", "Area Code", "Description"]
        super().__init__(AREA_CODE_MANAGER, "Area Codes", columns, AreaCodeDialog)

class DeviceTypeTable(SimpleTable):
    def __init__(self):
        columns = ["ID", "Device Type", "Description"]
        super().__init__(DEVICE_TYPE_MANAGER, "Device Types", columns, DeviceTypeDialog)
