from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class MultiSelectComboBox(QPushButton):
    def __init__(self, items, text="", parent=None):
        super().__init__(text, parent)

        # Store the items
        self.items = items

        # Create a menu for the drop-down
        self.menu = QMenu(self)

        # Create a list widget inside the menu
        self.list_widget = QListWidget()

        # Populate the list widget with the items and make them checkable
        for item in self.items:
            list_item = QListWidgetItem(item)
            list_item.setFlags(list_item.flags() | Qt.ItemIsUserCheckable)
            list_item.setCheckState(Qt.Unchecked)
            self.list_widget.addItem(list_item)

        # Add the list widget to the menu
        self.menu.setFixedWidth(200)  # Set the width of the menu
        self.menu.setFixedHeight(200)  # Set the height of the menu
        self.menu.setLayout(QVBoxLayout())
        self.menu.layout().addWidget(self.list_widget)

        # Set the menu to be shown when the button is clicked
        self.setMenu(self.menu)

    def get_selected_items(self):
        selected_items = []
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            if item.checkState() == Qt.Checked:
                selected_items.append(item.text())
        return selected_items