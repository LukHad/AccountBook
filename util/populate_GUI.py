from TransactionBook.model.TransactionBook import TransactionBook
import sys
from PySide2.QtWidgets import QApplication
from TransactionBook.Controller import Controller

tb = TransactionBook()
for i in range(0, 5):
    tb.new_transaction("01.07.2017", "Account 1", "My first transaction", 1000, "Income")

application = QApplication(sys.argv)
ctrl = Controller()

ctrl.model = tb
ctrl.view.update_data()

ctrl.view.show()
sys.exit(application.exec_())


