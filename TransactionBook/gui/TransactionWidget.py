import sys

from PySide2.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QHBoxLayout


class TransactionWidget(QWidget):
    def __init__(self):
        super(TransactionWidget, self).__init__()
        self.name = "Transactions"

        layout = QHBoxLayout()
        self.table = QTableWidget(3, 3)
        # self.columnLabels = ["Make", "Model", "Price"]
        # self.table.setHorizontalHeaderLabels(self.columnLabels)

        # test_table_content = QTableWidgetItem("Test data")
        # self.table.setItem(4, 1, test_table_content)

        layout.addWidget(self.table)
        self.setLayout(layout)

