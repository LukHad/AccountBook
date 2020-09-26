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

        self.ctrl.debug_print(f"View: Cell ({row}, {column}) / field {field} changed to {new_content}")
        # Write to data base
        self.ctrl.event_transaction_changed(row, field, new_content)

    def update_data(self):
        self.send_callbacks = False
        column_headings, data = self.ctrl.get_table_data()
        self.column_labels = column_headings
        num_columns = len(column_headings)

        table = self.table
        table.setColumnCount(num_columns)
        table.setHorizontalHeaderLabels(column_headings)

        num_rows = len(data)
        table.setRowCount(num_rows)
        for column in range(num_columns):
            for row in range(num_rows):
                col_label = self.column_labels[column]
                # For different columns different widgets are necessary to restrict possible cell values
                if col_label == self.ctrl.get_account_name():  # ACCOUNT
                    account_combo_box = QCustomComboBox(self.ctrl.get_account_list,
                                                        self.cb_item_changed,
                                                        row=row,
                                                        column=column
                                                        )
                    account_combo_box.set_text(data[row][column])
                    table.setCellWidget(row, column, account_combo_box)
                elif col_label == self.ctrl.get_category_name():  # CATEGORY
                    category_combo_box = QCustomComboBox(self.ctrl.get_category_list,
                                                         self.cb_item_changed,
                                                         row=row,
                                                         column=column
                                                         )
                    category_combo_box.set_text(data[row][column])
                    table.setCellWidget(row, column, category_combo_box)
                elif col_label == self.ctrl.get_amount_name():
                    amount_widget = QAmountSpinBox(self.ctrl.get_currency,
                                                   self.cb_item_changed,
                                                   row=row,
                                                   column=column
                                                   )
                    amount_widget.setValue(data[row][column])
                    table.setCellWidget(row, column, amount_widget)
                else:
                    table_item = QTableWidgetItem()
                    table_item.setData(Qt.DisplayRole, data[row][column])
                    table.setItem(row, column, table_item)
        self.send_callbacks = True


class QAmountSpinBox(QDoubleSpinBox):
    def __init__(self, get_currency_function, double_changed_callback=None, row=None, column=None):
        super(QAmountSpinBox, self).__init__()
        self.setMaximum(9999999.99)
        self.setMinimum(-9999999.99)
        self.setSuffix(f" {get_currency_function()}")

        self.tbl_row = row
        self.tbl_column = column

        if double_changed_callback is not None:
            self.valueChanged.connect(lambda: double_changed_callback(self))

    def row(self):
        return self.tbl_row

    def column(self):
        return self.tbl_column

    def text(self):
        return self.value()  # ToDo: Fix this workaround .text() should not return a float


class QCustomComboBox(QComboBox):
    def __init__(self, get_list_function, selection_changed_callback=None, row=None, column=None):
        super(QCustomComboBox, self).__init__()
        self.setStyleSheet("QComboBox { background-color: white; }")

        self.list_fun = get_list_function
        self.update_data()

        self.tbl_row = row
        self.tbl_column = column

        if selection_changed_callback is not None:
            self.currentIndexChanged.connect(lambda: selection_changed_callback(self))

    def row(self):
        return self.tbl_row

    def column(self):
        return self.tbl_column

    def set_text(self, text):
        item_list = self.list_fun()
        index = item_list.index(text)
        self.setCurrentIndex(index)

    def update_data(self):
        self.clear()
        item_list = self.list_fun()
        for el in item_list:
            self.addItem(el)

    def text(self):
        return self.itemText(self.currentIndex())


class NewTransactionPopUp(QWidget):
    def __init__(self, ctrl, parent=None):
        super(NewTransactionPopUp, self).__init__()
        self.name = "New Transaction"
        self.setWindowTitle(self.name)
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
        self.account_input = QCustomComboBox(self.ctrl.get_account_list)
        self.description_input = QLineEdit()
        self.amount_input = QAmountSpinBox(self.ctrl.get_currency)
        self.category_input = QCustomComboBox(self.ctrl.get_category_list)
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
        account = self.account_input.text()
        description = self.description_input.text()
        amount = self.amount_input.value()
        category = self.category_input.text()
        self.ctrl.debug_print(f"Date: {date}")
        self.ctrl.debug_print(f"account: {account}")
        self.ctrl.debug_print(f"description: {description}")
        self.ctrl.debug_print(f"amount: {amount}, Type: {type(amount)}")
        self.ctrl.debug_print(f"category: {category}")

        # ToDo: Validate input e.g. no empty field
        self.ctrl.event_new_transaction(date, account, description, amount, category)
        self.close()







