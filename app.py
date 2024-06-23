import sys
from PySide6.QtWidgets import QTableWidget, QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QLabel, QDockWidget, QSplitter, QLineEdit, QPushButton, QFileDialog, QMessageBox, QTableWidgetItem
from PySide6.QtCore import Qt
import pandas as pd

from db_classes import AreaCode, Equipment
from qt_table import AreaCodeTable, DeviceTypeTable
from db_setup import AREA_CODE_MANAGER, EQUIPMENT_MANAGER, DEVICE_TYPE_MANAGER, ValidationError


class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("Home Page")
        layout.addWidget(label)
        self.setLayout(layout)


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("Settings Page")
        layout.addWidget(label)
        self.setLayout(layout)


class ImportEquipmentPage(QWidget):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Import Equipment")

        # Create table widget
        self.table_widget = QTableWidget()
        
        # Create import button
        self.import_button = QPushButton("Import Equipment File")
        self.import_button.clicked.connect(self.open_file_dialog)

        # Create approve and import button
        self.approve_button = QPushButton("Approve and Import Equipment")
        self.approve_button.setEnabled(False)
        self.approve_button.clicked.connect(self.approve_and_import)

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(self.import_button)
        layout.addWidget(self.table_widget)
        layout.addWidget(self.approve_button)

        self.setLayout(layout)

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "CSV Files (*.csv);;Excel Files (*.xlsx)")
        if file_path:
            self.load_file(file_path)

    def load_file(self, file_path):
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            QMessageBox.warning(self, "Invalid File", "Please select a valid CSV or Excel file.")
            return

        self.populate_table(df)

    def populate_table(self, df):
        self.table_widget.setRowCount(df.shape[0])
        self.table_widget.setColumnCount(df.shape[1])
        self.table_widget.setHorizontalHeaderLabels(df.columns)

        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                item = QTableWidgetItem(str(df.iat[i, j]))
                self.table_widget.setItem(i, j, item)

        self.approve_button.setEnabled(True)

    def approve_and_import(self):
        rows = self.table_widget.rowCount()
        cols = self.table_widget.columnCount()

        errors = []
        for row in range(rows):
            data = {}
            for col in range(cols):
                header = self.table_widget.horizontalHeaderItem(col).text()
                data[header] = self.table_widget.item(row, col).text()

            # Create a new equipment entry
            new_equipment = Equipment(**data)
            try:
                self.manager.add(new_equipment)
            except ValidationError as e:
                errors.append(f"Row {row+1}: {str(e)}")

        if errors:
            QMessageBox.warning(self, "Import Errors", "\n".join(errors))
        else:
            QMessageBox.information(self, "Success", "Equipment imported successfully.")
            self.table_widget.setRowCount(0)
            self.table_widget.setColumnCount(0)
            self.approve_button.setEnabled(False)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(1000, 200, 720, 480)

        # Create tabs
        self.tab_widget = QTabWidget()
        self.home_page = HomePage()
        self.settings_page = SettingsPage()
        self.area_code_table_page = AreaCodeTable()
        self.device_type_table_page = DeviceTypeTable()
        self.import_equipment_page = ImportEquipmentPage(EQUIPMENT_MANAGER)

        self.tab_widget.addTab(self.home_page, "Home")
        self.tab_widget.addTab(self.settings_page, "Settings")
        self.tab_widget.addTab(self.area_code_table_page, "Area Codes")
        self.tab_widget.addTab(self.device_type_table_page, "Device Types")
        self.tab_widget.addTab(self.import_equipment_page, "Import Equipment")

        # Add tabs to the main window
        self.setCentralWidget(self.tab_widget)

        # Create docks for draggable tabs
        self.create_dock(self.area_code_table_page, "Area Codes")
        self.create_dock(self.device_type_table_page, "Device Types")

    def create_dock(self, widget, title):
        dock = QDockWidget(title, self)
        dock.setWidget(widget)
        dock.setFloating(False)  # Start docked by default
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock)


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
