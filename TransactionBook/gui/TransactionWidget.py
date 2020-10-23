import sys

from PySide2.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QGridLayout, QLabel, QLineEdit, \
                              QPushButton, QAbstractItemView, QInputDialog
from PySide2.QtCore import Qt

from TransactionBook.gui.QCustomWidgets import QCustomComboBox, QAmountSpinBox, QCustomCalendarWidget


class TransactionTableWidget(QWidget):
    def __init__(self, ctrl):
        super(TransactionTableWidget, self).__init__()
        self.name = "Transactions"
        self.ctrl = ctrl

        self.table = QTableWidget(3, 3)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Set to read only

        self.year_label = QLabel("Year: ")
        self.month_label = QLabel("Month: ")
        self.year_selector = QCustomComboBox(self.ctrl.get_years_in_data_as_str,
                                             self.ctrl.event_selected_transaction_year_changed)
        self.month_selector = QCustomComboBox(self.ctrl.get_months_as_str,
                                              self.ctrl.event_selected_transaction_month_changed)

        layout = QGridLayout()
        layout.addWidget(self.year_label, 0, 0)
        layout.addWidget(self.year_selector, 0, 1)
        layout.addWidget(self.month_label, 0, 2)
        layout.addWidget(self.month_selector, 0, 3)
        layout.addWidget(self.table, 1, 0, 1, 16)
        self.setLayout(layout)

        # self.update_data()

    def update_data(self):
        # Transaction table
        column_headings, data = self.ctrl.get_transaction_table_data()
        num_columns = len(column_headings)

        table = self.table
        table.setColumnCount(num_columns)
        table.setHorizontalHeaderLabels(column_headings)

        num_rows = len(data)
        table.setRowCount(num_rows)
        for column in range(num_columns):
            for row in range(num_rows):
                table_item = QTableWidgetItem()
                if column == 3:  # Special handling for amount column  # ToDo: Not nice doing it by index
                    table_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    if data[row][column] < 0.0:
                        table_item.setTextColor(Qt.red)
                    data[row][column] = self.ctrl.get_pretty_amount_str(data[row][column])  # cast to string
                table_item.setData(Qt.DisplayRole, data[row][column])
                table.setItem(row, column, table_item)
        table.resizeColumnsToContents()

        # Dop downs
        self.year_selector.update_data()
        self.month_selector.update_data()


class TransactionPopUp(QWidget):
    def __init__(self, ctrl, edit_transaction_id=None):
        super(TransactionPopUp, self).__init__()
        self.ctrl = ctrl
        self.edit_transaction_id = edit_transaction_id

        layout = QGridLayout(self)
        self.setLayout(layout)

        # Create GUI elements
        # - Labels
        self.date_label = QLabel("Date: ")
        self.account_label = QLabel("Account: ")
        self.description_label = QLabel("Description: ")
        self.amount_label = QLabel("Amount: ")
        self.category_label = QLabel("Category: ")
        # - Inputs
        self.date_input = QCustomCalendarWidget(date_time_format=self.ctrl.get_date_time_format())
        self.account_input = QCustomComboBox(self.ctrl.get_account_list)
        self.description_input = QLineEdit()
        self.amount_input = QAmountSpinBox(self.ctrl.get_currency)
        self.category_input = QCustomComboBox(self.ctrl.get_category_list)
        self.add_account_btn = QPushButton("Add")
        self.add_category_btn = QPushButton("Add")
        self.ok_btn = QPushButton("OK")
        self.cancel_btn = QPushButton("Cancel")

        # Add button callbacks
        self.ok_btn.clicked.connect(self.cb_ok)
        self.cancel_btn.clicked.connect(self.close)
        self.add_account_btn.clicked.connect(self.cb_add_account)
        self.add_category_btn.clicked.connect(self.cb_add_category)

        if self.edit_transaction_id is not None:
            self.init_edit_transaction()
            self.setWindowTitle("Edit Transaction")
        else:
            self.setWindowTitle("New Transaction")

        layout.addWidget(self.date_label, 0, 0)
        layout.addWidget(self.date_input, 0, 1, 1, 2)
        layout.addWidget(self.account_label, 1, 0)
        layout.addWidget(self.account_input, 1, 1)
        layout.addWidget(self.add_account_btn, 1, 2)
        layout.addWidget(self.description_label, 2, 0)
        layout.addWidget(self.description_input, 2, 1)
        layout.addWidget(self.amount_label, 3, 0)
        layout.addWidget(self.amount_input, 3, 1)
        layout.addWidget(self.category_label, 4, 0)
        layout.addWidget(self.category_input, 4, 1)
        layout.addWidget(self.add_category_btn, 4, 2)
        layout.addWidget(self.ok_btn, 5, 0)
        layout.addWidget(self.cancel_btn, 5, 2)

        self.resize(600, 200)

    def init_edit_transaction(self):
        date, account, description, amount, category = self.ctrl.get_transaction_from_view_id(self.edit_transaction_id)
        self.date_input.set_date_from_text(date)
        self.account_input.set_text(account)
        self.description_input.setText(description)
        self.amount_input.setValue(amount)
        self.category_input.set_text(category)

    def cb_ok(self):
        date = self.date_input.text()
        account = self.account_input.text()
        description = self.description_input.text()
        amount = self.amount_input.value()
        category = self.category_input.text()

        # # Validate input
        # if description == "":
        #     msg_box = QMessageBox()
        #     msg_box.setText("The field <Description> is not allowed to be empty")
        #     msg_box.exec_()
        #     return

        if self.edit_transaction_id is None:
            self.ctrl.event_new_transaction(date, account, description, amount, category)
        else:
            self.ctrl.event_edit_transaction(self.edit_transaction_id, date, account, description, amount, category)
        self.close()

    def cb_add_category(self):
        text, ok = QInputDialog.getText(self, 'New Category', 'Info: A new category is only saved when it is assigned \n'
                                                              'to at least one transaction. \n\n'
                                                              'Enter new category name:')
        if ok:
            self.ctrl.event_add_category(text)
            self.category_input.update_data()
            self.category_input.set_text(text)

    def cb_add_account(self):
        text, ok = QInputDialog.getText(self, 'New Account', 'Info: A new account is only saved when it is assigned \n'
                                                             'to at least one transaction. \n\n'
                                                             'Enter new account name:')
        if ok:
            self.ctrl.event_add_account(text)
            self.account_input.update_data()
            self.account_input.set_text(text)







