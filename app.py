import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QLabel
)
from db_setup import EQUIPMENT_MANAGER, AREA_CODE_MANAGER, DEVICE_TYPE_MANAGER
from equipment_entry_page import EquipmentEntryPage
from import_equipment_page import ImportEquipmentPage
from qt_table import AreaCodeTable, DeviceTypeTable

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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(1000, 200, 720, 480)

        # Create tabs
        self.tab_widget = QTabWidget()
        self.home_page = HomePage()
        self.settings_page = SettingsPage()
        self.import_equipment_page = ImportEquipmentPage(EQUIPMENT_MANAGER)
        self.equipment_entry_page = EquipmentEntryPage(EQUIPMENT_MANAGER, AREA_CODE_MANAGER, DEVICE_TYPE_MANAGER)
        self.area_code_table = AreaCodeTable()
        self.device_type_table = DeviceTypeTable()

        self.tab_widget.addTab(self.home_page, "Home")
        self.tab_widget.addTab(self.settings_page, "Settings")
        self.tab_widget.addTab(self.import_equipment_page, "Import Equipment")
        self.tab_widget.addTab(self.equipment_entry_page, "Enter Equipment")
        self.tab_widget.addTab(self.area_code_table, "Area Codes")
        self.tab_widget.addTab(self.device_type_table, "Device Types")

        # Add tabs to the main window
        self.setCentralWidget(self.tab_widget)

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
