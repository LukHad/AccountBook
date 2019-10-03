import os
from tests.test_TransactionBook import dummy_transactions_2
from TransactionBook.gui_kivy.AppMain import AppMain

main = AppMain()
main.display_controller.model = dummy_transactions_2()
main.display_controller.model.populate_lists_from_data()
# main.display_controller.model.path = os.path.join("saved_data", "DummyTransactionData.csv")
# main.display_controller.model.load()
main.run()


