from PySide2.QtWidgets import  QComboBox, QDoubleSpinBox, QCalendarWidget
from PySide2.QtCore import QDate


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


class QCustomCalendarWidget(QCalendarWidget):
    def __init__(self, date_time_format):
        super(QCustomCalendarWidget, self).__init__()
        self.setGridVisible(True)
        self.date_time_format = date_time_format

    def set_date_from_text(self, date_str):
        date = QDate.fromString(date_str, self.date_time_format)
        self.setSelectedDate(date)

    def text(self):
        return self.selectedDate().toString(self.date_time_format)