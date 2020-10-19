from PySide2.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QGridLayout,  QAbstractItemView
from PySide2.QtCore import Qt

from PySide2.QtCharts import QtCharts


class AccountTableWidget(QWidget):
    def __init__(self, ctrl):
        super(AccountTableWidget, self).__init__()
        self.name = "Accounts"
        self.ctrl = ctrl

        # Transaction table
        self.acc_table = QTableWidget(3, 3)
        self.acc_table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Set to read only
        self.acc_table.verticalHeader().setVisible(False)

        # Account Pie
        self.acc_chart = QtCharts.QChart()
        self.acc_pie = QtCharts.QChartView(self.acc_chart)

        # Total balance over months
        self.balance_trend_chart = QtCharts.QChart()
        self.balance_trend_view = QtCharts.QChartView(self.balance_trend_chart)
        self.balance_trend_y_axis = None

        layout = QGridLayout()
        layout.addWidget(self.acc_table, 0, 0)
        layout.addWidget(self.acc_pie, 0, 1)
        layout.addWidget(self.balance_trend_view, 1, 0, 1, 2)

        self.setLayout(layout)
        self.update_data()

    def update_data(self):
        acc_data_dict = self.ctrl.get_account_data()

        # Account Table
        #  Create table data
        data = []
        total_balance = 0
        for key, value in acc_data_dict.items():
            total_balance += value
            data.append([key, str(value) + " " + self.ctrl.get_currency()])
        #  Add empty row
        data.append(["", ""])
        #  Add sum to data
        data.append(["Total balance", str(round(total_balance, 2)) + " " + self.ctrl.get_currency()])
        #  Create table widget
        column_headings = ["Accounts", "Balance"]
        num_columns = len(column_headings)
        table = self.acc_table
        table.setColumnCount(num_columns)
        table.setHorizontalHeaderLabels(column_headings)
        num_rows = len(data)
        table.setRowCount(num_rows)
        for column in range(num_columns):
            for row in range(num_rows):
                table_item = QTableWidgetItem()
                if column == 1:  # Align balance to the right with vertically centered
                    table_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                table_item.setData(Qt.DisplayRole, data[row][column])
                table.setItem(row, column, table_item)

        # Account Pie
        #  Reset
        self.acc_chart.removeAllSeries()
        self.acc_chart.setTitle("Accounts with positive balance")
        # self.acc_chart.legend().hide()
        series = QtCharts.QPieSeries()
        #  Add data
        for key in acc_data_dict.keys():
            add_balance = acc_data_dict[key]
            if add_balance > 0:
                series.append(key, add_balance)
        #  Add percentage labels
        # series.setLabelsVisible()
        # series.setLabelsPosition(QtCharts.QPieSlice.LabelInsideHorizontal)
        for my_slice in series.slices():
            percentage_str = "{:.1f}%".format(100 * my_slice.percentage())
            my_slice.setLabel(f"{my_slice.label()}({percentage_str})")

        self.acc_chart.addSeries(series)

        # Total balance trend
        self.balance_trend_chart.removeAllSeries()
        self.balance_trend_chart.removeAxis(self.balance_trend_y_axis)
        labels, results = self.ctrl.get_total_balance_trend()
        if results:
            series = QtCharts.QLineSeries()
            for i, _ in enumerate(labels):
                series.append(i, results[i])
                print(results[i])

            self.balance_trend_y_axis = QtCharts.QValueAxis()
            self.balance_trend_y_axis.setRange(min(results), max(results))
            self.balance_trend_chart.addSeries(series)
            self.balance_trend_chart.addAxis(self.balance_trend_y_axis, Qt.AlignLeft)
