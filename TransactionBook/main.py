import sys
from PySide2.QtWidgets import QApplication
from TransactionBook.gui.ViewManager import ViewManager

application = QApplication(sys.argv)
vm = ViewManager()
vm.main_window.show()

# Test
column_headings = ["Date", "Account", "Amount"]
data = [["08.09.2020", "Deutsche Bank", 120.0],
        ["10.09.2020", "Deutsche Bank", -120],
        ]
vm.set_transaction_table(column_headings, data)
# End Test ToDo: How to best implement Gui-Tests


sys.exit(application.exec_())
