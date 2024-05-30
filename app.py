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
)
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMainWindow, QMenu
from PySide6.QtCore import QSize, Qt

from db_setup import session
from db_managers import *




# # Subclass QMainWindow to customize your application's main window
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle("SadieWare")
#         self.setMinimumSize(QSize(960, 720))

#         self.area_code_manager = AreaCodeManager(session=session)
#         self.area_code_table_widget = QTableWidget()
#         area_codes = self.area_code_manager.get_all()

#         self.area_code_table_widget.setRowCount(len(area_codes))
#         self.area_code_table_widget.setColumnCount(2)
#         self.area_code_table_widget.setHorizontalHeaderLabels(["Area Code", "Description"])

#         for row, area_code in enumerate(area_codes):
#             self.area_code_table_widget.setItem(row, 0, QTableWidgetItem(area_code.area_code))
#             self.area_code_table_widget.setItem(row, 1, QTableWidgetItem(area_code.description))

#         layout = QVBoxLayout()
#         layout.addWidget(self.area_code_table_widget)

#         container = QWidget()
#         container.setLayout(layout)

#         self.setCentralWidget(container)
area_code_manager = AreaCodeManager(session)


class AreaCodeTable(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Area Codes")
        self.setGeometry(300, 100, 800, 600)

        # create and connect table
        self.table_widget = QTableWidget()
        self.table_widget.itemSelectionChanged.connect(self.update_button_states)
        self.table_widget.cellDoubleClicked.connect(self.edit_entry)
        self.load_data()

        # create and connect buttons
        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self.edit_entry)
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_entry)
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_entry)

        # Disable the edit and delete buttons initially
        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)
        
        # style buttons
        self.style_buttons()

        # create button layout
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addStretch()

        # create main layout
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)
        layout.addLayout(button_layout)

        # create main container widget
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

    def load_data(self):
        # prevent triggering signals while loading data
        self.table_widget.blockSignals(True)

        area_codes = area_code_manager.get_all()
        self.table_widget.setRowCount(len(area_codes))
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Area Code", "Description"])

        for row, area_code in enumerate(area_codes):
            area_code_item = QTableWidgetItem(area_code.area_code)
            area_code_item.setFlags(area_code_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table_widget.setItem(row, 0, area_code_item)

            description_item = QTableWidgetItem(area_code.description)
            description_item.setFlags(description_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table_widget.setItem(row, 1, description_item)

        # re-enable signals
        self.table_widget.blockSignals(False)

    def edit_entry(self, row=None, column=None):
        # for when row is double clicked
        if row is None:
            selected_row = self.table_widget.currentRow()
        # for when edit button is pressed
        else:
            selected_row = row

        if selected_row < 0:
            QMessageBox.warning(self, "No selection", "Please select a row to edit")
            return

        area_code_item = self.table_widget.item(selected_row, 0)
        description_item = self.table_widget.item(selected_row, 1)

        dialog = AreaCodeDialog(self, area_code_item.text(), description_item.text())
        if dialog.exec():
            area_code, description = dialog.get_data()
            area_code_id = area_code_manager.filter(lambda model: model.area_code == area_code_item.text())[0].id
            area_code_manager.update(area_code_id, {'area_code': area_code, 'description': description})
            self.load_data()

    def add_entry(self):
        dialog = AreaCodeDialog(self)
        if dialog.exec():
            area_code, description = dialog.get_data()
            new_area_code = AreaCode(area_code=area_code, description=description)
            area_code_manager.add(new_area_code)
            self.load_data()

    def delete_entry(self):
        selected_row = self.table_widget.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "No selection", "Please select a row to delete")
            return

        response = QMessageBox.question(self, "Confirm Delete", "Are you sure you want to delete this entry?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if response == QMessageBox.StandardButton.Yes:
            area_code_item = self.table_widget.item(selected_row, 0)
            area_code_id = area_code_manager.filter(lambda model: model.area_code == area_code_item.text())[0].id
            area_code_manager.delete(area_code_id)
            self.load_data()

    def update_button_states(self):
        has_selection = bool(self.table_widget.selectedItems())
        self.edit_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)



class AreaCodeDialog(QDialog):
    def __init__(self, parent=None, area_code='', description=''):
        super().__init__(parent)
        self.setWindowTitle('Area Code Details')

        self.area_code_edit = QLineEdit(area_code)
        self.description_edit = QLineEdit(description)

        form_layout = QFormLayout()
        form_layout.addRow(QLabel('Area Code:'), self.area_code_edit)
        form_layout.addRow(QLabel('Description:'), self.description_edit)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def get_data(self):
        return self.area_code_edit.text(), self.description_edit.text()


# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication([])


window = AreaCodeTable()
window.show()

# Start the event loop.
app.exec()

# Your application won't reach here until you exit and the event
# loop has stopped.
