from TransactionBook.gui.MainWindow import MainWindow
from TransactionBook.model.TransactionBook import TransactionBook


class Controller:
    def __init__(self):
        self.DEBUG = True
        self.model = TransactionBook()
        self.view = MainWindow(self)
        # Test
        self.model.load_from(r"C:\Users\Win10VM\Documents\MyLocalFiles\Python_Projects\TransactionBook\tests\test_database.csv")
        # End Test
        self.view.update_data()

    def debug_print(self, text):
        if self.DEBUG:
            print(text)

    def get_data_columns(self):
        df = self.model.get_data()
        columns = df.columns.tolist()
        columns.remove(self.model.ID)
        return columns

    def get_table_data(self):
        df = self.model.get_data()
        if not df.empty:
            # Convert date to string according to date format
            df[self.model.DATE] = df[self.model.DATE].dt.strftime(self.model.DATE_TIME_FORMAT)
            # Remove ID column from dataframe
            df = df.loc[:, df.columns != self.model.ID]
            data = df.values.tolist()
        else:
            data = []

        return data

    def event_transaction_changed(self, view_row, field, new_content):
        self.debug_print(f"In row {view_row} the field {field} changed to {new_content}")
        self.model.edit_transaction_field(view_row, field, new_content)
        self.view.update_data()

    def get_account_list(self):
        return self.model.get_accounts()

    def get_category_list(self):
        return self.model.get_categories()

    def get_currency(self):
        return self.model.CURRENCY
