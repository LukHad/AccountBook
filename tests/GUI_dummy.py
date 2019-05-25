from tests.test_TransactionBook import dummy_transactions

from src.gui_kivy.AppMain import AppMain

main = AppMain()
main.display_controller.model = dummy_transactions()
main.display_controller.model.populate_lists_from_data()
main.run()


