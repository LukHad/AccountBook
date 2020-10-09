from PySide2.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QGridLayout, QLabel, QLineEdit, \
                              QPushButton, QComboBox, QDoubleSpinBox, QAbstractItemView, QInputDialog, QCalendarWidget
from PySide2.QtCore import Qt, QPoint, QDate

from PySide2.QtCharts import QtCharts


class AccountTableWidget(QWidget):
    def __init__(self, ctrl):
        super(AccountTableWidget, self).__init__()
        self.name = "Accounts"
        self.ctrl = ctrl

        # Transaction table
        self.acc_table = QTableWidget(3, 3)
        self.acc_table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Set to read only

        # Account Pie
        self.acc_chart = QtCharts.QChart()
        self.acc_pie = QtCharts.QChartView(self.acc_chart)

        layout = QGridLayout()
        layout.addWidget(self.acc_table, 0, 0)
        layout.addWidget(self.acc_pie, 0, 1)

        self.setLayout(layout)
        self.update_data()

    def update_data(self):
        acc_data_dict = self.ctrl.get_account_data()
        # Table
        column_headings = ["Accounts", "Balance"]
        data = []
        for key, value in acc_data_dict.items():
            data.append([key, str(value) + " " + self.ctrl.get_currency()])
        num_columns = len(column_headings)

        table = self.acc_table
        table.setColumnCount(num_columns)
        table.setHorizontalHeaderLabels(column_headings)

        num_rows = len(data)
        table.setRowCount(num_rows)
        for column in range(num_columns):
            for row in range(num_rows):
                table_item = QTableWidgetItem()
                table_item.setData(Qt.DisplayRole, data[row][column])
                table.setItem(row, column, table_item)

        # Pie
        self.acc_chart.removeAllSeries()
        series = QtCharts.QPieSeries()
        for key in acc_data_dict.keys():
            series.append(key, acc_data_dict[key])

        self.acc_chart.addSeries(series)
