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

        layout = QGridLayout(self)
        self.setLayout(layout)

        date_label = QLabel("Date: ")
        account_label = QLabel("Account: ")
        description_label = QLabel("Description: ")
        amount_label = QLabel("Amount: ")
        category_label = QLabel("Category: ")

        date_input = QLineEdit()
        account_input = QComboBox()
        # Test
        account_input.addItem("Account 1")
        account_input.addItem("Account 2")
        # End Test
        description_input = QLineEdit()
        amount_input = QLineEdit()
        category_input = QLineEdit()

        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(view_manager.cb_new_transaction)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.close)

        layout.addWidget(date_label, 0, 0)
        layout.addWidget(date_input, 0, 1)
        layout.addWidget(account_label)
        layout.addWidget(account_input)
        layout.addWidget(description_label)
        layout.addWidget(description_input)
        layout.addWidget(amount_label)
        layout.addWidget(amount_input)
        layout.addWidget(category_label)
        layout.addWidget(category_input)
        layout.addWidget(ok_btn)
        layout.addWidget(cancel_btn)

        self.resize(600, 200)






