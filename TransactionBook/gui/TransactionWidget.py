import sys

from PySide2.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QHBoxLayout, QGridLayout, QLabel, QLineEdit, \
                              QPushButton, QComboBox
from PySide2.QtCore import Qt, QPoint

class TransactionTableWidget(QWidget):
    def __init__(self, view_manager):
        super(TransactionTableWidget, self).__init__()
        self.name = "Transactions"
        self.table = QTableWidget(3, 3)
        layout = QHBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)
        # Callbacks
        self.table.itemChanged.connect(view_manager.cb_transaction_changed)
        # self.table.itemDoubleClicked.connect(view_manager.cb_transaction_item_entered)


class NewTransactionPopUp(QWidget):
    def __init__(self, view_manager, parent=None):
        super(NewTransactionPopUp, self).__init__()
        self.setWindowTitle('Input dialog')
        self.view_manager = view_manager

        layout = QGridLayout(self)
        self.setLayout(layout)

        # Create GUI elements # ToDo: Add possiblity to add new categories and accounts
        # - Labels
        self.date_label = QLabel("Date: ")
        self.account_label = QLabel("Account: ")
        self.description_label = QLabel("Description: ")
        self.amount_label = QLabel("Amount: ")
        self.category_label = QLabel("Category: ")
        # - Inputs
        self.date_input = QLineEdit()
        self.account_input = QComboBox()
        self.description_input = QLineEdit()
        self.amount_input = QLineEdit() # ToDo: Allow only numbers
        self.category_input = QComboBox()
        self.ok_btn = QPushButton("OK")
        self.cancel_btn = QPushButton("Cancel")

        # Populate combo box
        view_manager.populate_account_combo_box(self.account_input)
        view_manager.populate_category_combo_box(self.category_input)
        # Add button callbacks
        self.ok_btn.clicked.connect(self.cb_ok)
        self.cancel_btn.clicked.connect(self.close)

        layout.addWidget(self.date_label, 0, 0)
        layout.addWidget(self.date_input, 0, 1)
        layout.addWidget(self.account_label)
        layout.addWidget(self.account_input)
        layout.addWidget(self.description_label)
        layout.addWidget(self.description_input)
        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_input)
        layout.addWidget(self.category_label)
        layout.addWidget(self.category_input)
        layout.addWidget(self.ok_btn)
        layout.addWidget(self.cancel_btn)

        self.resize(600, 200)

    def cb_ok(self):
        date = self.date_input.text()
        account = self.account_input.itemText(self.account_input.currentIndex())
        description = self.description_input.text()
        amount = self.amount_input.text()
        category = self.category_input.itemText(self.category_input.currentIndex())
        print(f"Date: {date}")
        print(f"account: {account}")
        print(f"description: {description}")
        print(f"amount: {amount}")
        print(f"category: {category}")
        self.view_manager.cb_new_transaction()







