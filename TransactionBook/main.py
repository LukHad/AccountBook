import sys
from PySide2.QtWidgets import QApplication
from TransactionBook.gui.ViewManager import ViewManager
from TransactionBook.model.TransactionBook import TransactionBook
from TransactionBook.Controller import Controller

application = QApplication(sys.argv)
ctrl = Controller()
ctrl.view.main_window.show()
sys.exit(application.exec_())
