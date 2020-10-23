from PySide2.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QGridLayout,  QAbstractItemView
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont
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
        acc_pie = QtCharts.QChartView(self.acc_chart)

        # Total balance over months
        self.balance_trend_chart = QtCharts.QChart()
        self.balance_trend_chart.legend().hide()
        balance_trend_view = QtCharts.QChartView(self.balance_trend_chart)
        self.balance_trend_y_axis = None
        self.balance_trend_x_axis = None

        # Monthly bar trend
        self.monthly_bar_chart = QtCharts.QChart()
        self.monthly_bar_chart.legend().hide()
        monthly_bar_view = QtCharts.QChartView(self.monthly_bar_chart)
        self.monthly_bar_chart_y_axis = None
        self.monthly_bar_chart_x_axis = None

        layout = QGridLayout()
        layout.addWidget(self.acc_table, 0, 0)
        layout.addWidget(acc_pie, 0, 1)
        layout.addWidget(balance_trend_view, 1, 0)
        layout.addWidget(monthly_bar_view, 1, 1)

        self.setLayout(layout)
        self.update_data()

    def update_data(self):
        self.update_account_table()
        self.update_account_pie()
        self.update_total_balance_trend()
        self.update_monthly_bar_trend()

    def update_account_table(self):
        acc_data_dict = self.ctrl.get_account_data()

        # Account Table
        #  Create table data
        data = []
        total_balance = 0
        column_headings = ["Accounts", "Balance"]
        table = self.acc_table
        table.setColumnCount(len(column_headings))
        table.setRowCount(len(acc_data_dict) + 1)  # +1 due to Total balance row
        table.setHorizontalHeaderLabels(column_headings)

        #  Add account data
        for i, (key, value) in enumerate(acc_data_dict.items()):
            total_balance += value
            data.append([key, value])

            table_item_key = QTableWidgetItem()
            table_item_value = QTableWidgetItem()
            table_item_value.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            if value < 0:
                table_item_value.setTextColor(Qt.red)

            value_str = self.ctrl.get_pretty_amount_str(value)

            table_item_key.setData(Qt.DisplayRole, key)
            table_item_value.setData(Qt.DisplayRole, value_str)
            table.setItem(i, 0, table_item_key)
            table.setItem(i, 1, table_item_value)

        #  Add total balance
        table_item_key = QTableWidgetItem()
        table_item_value = QTableWidgetItem()
        table_item_value.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        font = QFont().setBold(True)
        table_item_key.setFont(font)
        table_item_value.setFont(font)
        table_item_key.setData(Qt.DisplayRole, "Total balance")
        table_item_value.setData(Qt.DisplayRole, self.ctrl.get_pretty_amount_str(total_balance))

        table.setItem(len(acc_data_dict), 0, table_item_key)
        table.setItem(len(acc_data_dict), 1, table_item_value)

    def update_account_pie(self):
        acc_data_dict = self.ctrl.get_account_data()
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

    def update_total_balance_trend(self):
        self.balance_trend_chart.removeAllSeries()
        labels, results = self.ctrl.get_total_balance_trend()
        # Values
        if results:
            series = QtCharts.QLineSeries()
            # set properties
            # series.legend().hide()
            series.setPointsVisible(True)
            # set data
            for i, result in enumerate(results):
                series.append(i, result)
            # add to chart
            self.balance_trend_chart.addSeries(series)

            # y_Axis
            self.balance_trend_chart.removeAxis(self.balance_trend_y_axis)
            y_axis = QtCharts.QValueAxis()
            # set properties
            y_axis.setRange(min(results), max(results))
            y_axis.setLabelFormat("%.0f")
            y_axis.setTitleText(f"Total balance [{self.ctrl.get_currency()}]")
            self.balance_trend_y_axis = y_axis
            self.balance_trend_chart.addAxis(y_axis, Qt.AlignLeft)

            # x_Axis
            self.balance_trend_chart.removeAxis(self.balance_trend_x_axis)
            x_axis = QtCharts.QBarCategoryAxis()
            # set properties
            x_axis.append(labels)
            x_axis.setLabelsAngle(-90)
            self.balance_trend_x_axis = x_axis
            self.balance_trend_chart.addAxis(x_axis, Qt.AlignBottom)

    def update_monthly_bar_trend(self):
        self.monthly_bar_chart.removeAllSeries()
        labels, results = self.ctrl.get_monthly_bar_trend()
        if results:
            series = QtCharts.QBarSeries()
            bar_set = QtCharts.QBarSet("Test")
            for i, result in enumerate(results):
                bar_set.append(result)

            # ToDo: Negative bars shall be red
            series.append(bar_set)
            self.monthly_bar_chart.addSeries(series)

            # y_Axis
            self.monthly_bar_chart.removeAxis(self.monthly_bar_chart_y_axis)
            y_axis = QtCharts.QValueAxis()
            # set properties
            y_axis.setRange(min(results), max(results))
            y_axis.setLabelFormat("%.0f")
            y_axis.setTitleText(f"Monthly balance [{self.ctrl.get_currency()}]")

            self.monthly_bar_chart.addAxis(y_axis, Qt.AlignLeft)
            self.monthly_bar_chart_y_axis = y_axis

            # x_Axis
            self.monthly_bar_chart.removeAxis(self.monthly_bar_chart_x_axis)
            x_axis = QtCharts.QBarCategoryAxis()
            # set properties
            x_axis.append(labels)
            x_axis.setLabelsAngle(-90)
            self.monthly_bar_chart_x_axis = x_axis
            self.monthly_bar_chart.addAxis(x_axis, Qt.AlignBottom)






