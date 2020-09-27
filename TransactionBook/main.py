import sys
from PySide2.QtWidgets import QApplication
from TransactionBook.Controller import Controller

application = QApplication(sys.argv)
ctrl = Controller()
# Test
# ctrl.model.load_from(r"C:\Users\Win10VM\Documents\MyLocalFiles\Python_Projects\TransactionBook\util\dummy_database.csv")
# ctrl.view.update_data()
# End Test

ctrl.view.show()

sys.exit(application.exec_())
