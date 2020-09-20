from PySide2.QtWidgets import QTableWidgetItem
from PySide2.QtCore import Qt
from TransactionBook.gui.MainWindow import MainWindow


class ViewManager:
    def __init__(self, ctrl):
        self.main_window = MainWindow(self)
        self.send_callbacks = True
        self.ctrl = ctrl

        self.transaction_table_header_labels = []

    def set_transaction_table(self, column_headings, data):
        self.send_callbacks = False
        num_rows = len(data)
        num_columns = len(data[0])
        assert num_columns == len(column_headings), \
            "ViewManager.set_transaction_table: Number of column headings must match the columns in data"
        self.transaction_table_header_labels = column_headings
        table = self.main_window.transaction_widget.table
        table.setColumnCount(num_columns)
        table.setRowCount(num_rows)
        table.setHorizontalHeaderLabels(column_headings)

        for row in range(num_rows):
            for column in range(num_columns):
                table_item = QTableWidgetItem()
                table_item.setData(Qt.DisplayRole, data[row][column])
                # table_item.setFlags(Qt.ItemIsEnabled)
                table.setItem(row, column, table_item)

        self.send_callbacks = True

    def cb_transaction_changed(self, item):
        if self.send_callbacks:
            new_content = item.text()
            row = item.row()
            column = item.column()
            field = self.transaction_table_header_labels[column]
            self.ctrl.event_transaction_changed(row, field, new_content)


