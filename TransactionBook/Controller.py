from TransactionBook.gui.ViewManager import ViewManager
from TransactionBook.model.TransactionBook import TransactionBook


class Controller:
    def __init__(self):
        self.DEBUG = True
        self.model = TransactionBook()
        self.view = ViewManager(self)
        # Test
        self.model.load_from(r"C:\Users\Win10VM\Documents\MyLocalFiles\Python_Projects\TransactionBook\tests\test_database.csv")
        # End Test
        self.populate_transaction_view()

    def debug_print(self, text):
        if self.DEBUG:
            print(text)

    def update_view(self):
        self.populate_transaction_view()
        self.debug_print("View Updated")

    def populate_transaction_view(self):
        df = self.model.get_data()
        # Convert date to string according to date format
        df[self.model.DATE] = df[self.model.DATE].dt.strftime(self.model.DATE_TIME_FORMAT)
        # Remove ID column from dataframe
        df = df.loc[:, df.columns != self.model.ID]
        # Get column headings and data as a lost
        columns = df.columns
        data = df.values.tolist()

        self.view.set_transaction_table(columns, data)

    def event_transaction_changed(self, view_row, field, new_content):
        self.debug_print(f"In row {view_row} the field {field} changed to {new_content}")
        self.model.edit_transaction_field(view_row, field, new_content)
        self.update_view()

    def get_account_list(self):
        return self.model.get_accounts()

    def get_category_list(self):
        return self.model.get_categories()
