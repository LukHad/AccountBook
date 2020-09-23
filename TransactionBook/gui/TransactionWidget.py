import sys

from PySide2.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QHBoxLayout, QGridLayout, QLabel, QLineEdit, \
                              QPushButton, QComboBox, QDoubleSpinBox
from PySide2.QtCore import Qt, QPoint


class TransactionTableWidget(QWidget):
    def __init__(self, ctrl):
        super(TransactionTableWidget, self).__init__()
        self.name = "Transactions"
        self.ctrl = ctrl
        self.send_callbacks = True
        self.column_labels = []

        self.table = QTableWidget(3, 3)
        self.table.itemChanged.connect(self.cb_item_changed)

        layout = QHBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.update_data()

    def cb_item_changed(self, item):
        if not self.send_callbacks:
            return
        new_content = item.text()
        row = item.row()
        column = item.column()
        field = self.column_labels[column]
        self.ctrl.event_transaction_changed(row, field, new_content)

    def update_data(self):
        self.send_callbacks = False
        column_headings = self.ctrl.get_data_columns()
        self.column_labels = column_headings
        data = self.ctrl.get_table_data()
        num_columns = len(column_headings)

        table = self.table
        table.setColumnCount(num_columns)
        table.setHorizontalHeaderLabels(column_headings)

        num_rows = len(data)
        table.setRowCount(num_rows)
        for row in range(num_rows):
            for column in range(num_columns):
                table_item = QTableWidgetItem()
                table_item.setData(Qt.DisplayRole, data[row][column])
                # table_item.setFlags(Qt.ItemIsEnabled) # Make table read only
                #table.setEditTriggers(QAbstractItemView.NoEditTriggers)
                table.setItem(row, column, table_item)
        self.send_callbacks = True


class QAmountSpinBox(QDoubleSpinBox):
    def __init__(self, ctrl):
        super(QAmountSpinBox, self).__init__()
        self.setMaximum(9999999.99)
        self.setMinimum(-9999999.99)
        self.setSuffix(f" {ctrl.get_currency()}")


class QCategoryComboBox(QComboBox):
    def __init__(self, ctrl):
        super(QCategoryComboBox, self).__init__()
        self.ctrl = ctrl
        self.update_data()

    def update_data(self):
        category_list = self.ctrl.get_category_list()
        for category in category_list:
            self.addItem(category)


class QAccountComboBox(QComboBox):
    def __init__(self, ctrl):
        super(QAccountComboBox, self).__init__()
        self.ctrl = ctrl
        self.update_data()

    def update_data(self):
        account_list = self.ctrl.get_account_list()
        for account in account_list:
            self.addItem(account)


class NewTransactionPopUp(QWidget):
    def __init__(self, ctrl, parent=None):
        super(NewTransactionPopUp, self).__init__()
        self.setWindowTitle('Input dialog')
        self.ctrl = ctrl

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
        self.account_input = QAccountComboBox(ctrl)
        self.description_input = QLineEdit()
        self.amount_input = QAmountSpinBox(ctrl)
        self.category_input = QCategoryComboBox(ctrl)
        self.ok_btn = QPushButton("OK")
        self.cancel_btn = QPushButton("Cancel")

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
        amount = self.amount_input.value()
        category = self.category_input.itemText(self.category_input.currentIndex())
        print(f"Date: {date}")
        print(f"account: {account}")
        print(f"description: {description}")
        print(f"amount: {amount}, Type: {type(amount)}")
        print(f"category: {category}")








