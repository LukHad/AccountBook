import sys
from PySide2.QtWidgets import QApplication
from TransactionBook.Controller import Controller

application = QApplication(sys.argv)
ctrl = Controller()
ctrl.view.show()
sys.exit(application.exec_())
