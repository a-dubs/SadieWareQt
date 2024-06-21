import sys
from PySide6.QtWidgets import QTableWidget, QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QLabel, QDockWidget, QSplitter
from PySide6.QtCore import Qt

from db_classes import AreaCode
from qt_table import AreaCodeTable, DeviceTypeTable
from db_setup import *


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
        self.setGeometry(
            1000,
            200,
            720,
            480,
        )

        # Create tabs
        self.tab_widget = QTabWidget()
        # self.home_page = HomePage()
        # self.settings_page = SettingsPage()
        self.area_code_table_page = AreaCodeTable()
        self.device_type_table_page = DeviceTypeTable()

        # self.tab_widget.addTab(self.home_page, "Home")
        self.tab_widget.addTab(self.area_code_table_page, "Area Codes")
        self.tab_widget.addTab(self.device_type_table_page, "Device Types")
        # self.tab_widget.addTab(self.settings_page, "Settings")

        # Add tabs to the main window
        self.setCentralWidget(self.tab_widget)

        # Create docks for draggable tabs
        # self.create_dock(self.home_page, "Home")
        # self.create_dock(self.settings_page, "Settings")
        self.create_dock(self.area_code_table_page, "Area Codes")
        self.create_dock(self.device_type_table_page, "Device Types")

    def create_dock(self, widget, title):
        dock = QDockWidget(title, self)
        dock.setWidget(widget) 
        dock.setFloating(False)  # Start docked by default
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock)

        # self.tab_widget = QTabWidget()
        # self.tab_widget.addTab(HomePage(), "Home")
        # self.tab_widget.addTab(SettingsPage(), "Settings")
        # self.tab_widget.addTab(AreaCodeTable(), "Area Code Table")
        # self.tab_widget.addTab(DeviceTypeTable(), "Device Type Table")

        # # Create a splitter for drag-and-drop functionality
        # self.splitter = QSplitter(Qt.Horizontal)
        # self.splitter.addWidget(self.tab_widget)
        # self.setCentralWidget(self.splitter)

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
