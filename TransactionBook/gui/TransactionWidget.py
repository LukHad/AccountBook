import sys

from PySide2.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QHBoxLayout, QGridLayout, QLabel, QLineEdit, \
                              QPushButton, QComboBox, QDoubleSpinBox, QAbstractItemView
from PySide2.QtCore import Qt, QPoint


class TransactionTableWidget(QWidget):
    def __init__(self, ctrl):
        super(TransactionTableWidget, self).__init__()
        self.name = "Transactions"
        self.ctrl = ctrl
        self.column_labels = []

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

        self.update_data()

    def update_data(self):
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
                table_item = QTableWidgetItem()
                table_item.setData(Qt.DisplayRole, data[row][column])
                table.setItem(row, column, table_item)

        self.year_selector.update_data()
        self.month_selector.update_data()


class QAmountSpinBox(QDoubleSpinBox):
    def __init__(self, get_currency_function, double_changed_callback=None):
        super(QAmountSpinBox, self).__init__()
        self.setMaximum(9999999.99)
        self.setMinimum(-9999999.99)
        self.setSuffix(f" {get_currency_function()}")

        if double_changed_callback is not None:
            self.valueChanged.connect(lambda: double_changed_callback(self))


class QCustomComboBox(QComboBox):
    def __init__(self, get_list_function, selection_changed_callback=None):
        super(QCustomComboBox, self).__init__()
        #  self.setStyleSheet("QComboBox { background-color: white; }")

        self.list_fun = get_list_function
        self.selection_changed_callback = selection_changed_callback
        self.trigger_callbacks = True

        self.update_data()

        if selection_changed_callback is not None:
            self.currentIndexChanged.connect(self.cb_selection_changed)

    def set_text(self, text):
        item_list = self.list_fun()
        index = item_list.index(text)
        self.setCurrentIndex(index)

    def cb_selection_changed(self):
        if self.trigger_callbacks:
            self.selection_changed_callback(self.text())

    def update_data(self):
        old_text = self.text()
        item_list = self.list_fun()
        new_index = 0
        callback_necessary = True
        if old_text in item_list:
            new_index = item_list.index(old_text)
            callback_necessary = False

        self.trigger_callbacks = False  # Disable callbacks during list update
        self.clear()
        for el in item_list:
            self.addItem(el)

        if callback_necessary:
            self.trigger_callbacks = True  # Only trigger callback if selection actually changed
            self.setCurrentIndex(new_index)
        else:
            self.setCurrentIndex(new_index)

        self.trigger_callbacks = True

    def text(self):
        return self.itemText(self.currentIndex())


class TransactionPopUp(QWidget):
    def __init__(self, ctrl, edit_transaction_id=None):
        super(TransactionPopUp, self).__init__()
        self.ctrl = ctrl
        self.edit_transaction_id = edit_transaction_id

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

        if self.edit_transaction_id is not None:
            self.init_edit_transaction()
            self.setWindowTitle("Edit Transaction")
        else:
            self.setWindowTitle("New Transaction")

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

    def init_edit_transaction(self):
        date, account, description, amount, category = self.ctrl.get_transaction_from_view_id(self.edit_transaction_id)
        self.date_input.setText(date)
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
        self.ctrl.debug_print(f"Date: {date}")
        self.ctrl.debug_print(f"account: {account}")
        self.ctrl.debug_print(f"description: {description}")
        self.ctrl.debug_print(f"amount: {amount}, Type: {type(amount)}")
        self.ctrl.debug_print(f"category: {category}")

        # ToDo: Validate input e.g. no empty field
        if self.edit_transaction_id is None:
            self.ctrl.event_new_transaction(date, account, description, amount, category)
        else:
            self.ctrl.event_edit_transaction(self.edit_transaction_id, date, account, description, amount, category)
        self.close()







