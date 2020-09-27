import os

from TransactionBook.gui.MainWindow import MainWindow
from TransactionBook.model.TransactionBook import TransactionBook


class Controller:
    def __init__(self):
        self.DEBUG = True
        self.file_path = None
        self.file_name = "Transaction Book"
        self.selected_year = None
        self.selected_month = None

        self.model = TransactionBook()
        self.view = MainWindow(self)
        self.view.update_data()


    def debug_print(self, text):
        if self.DEBUG:
            print(text)

    def get_table_data(self):
        df = self.model.get_data()
        columns = df.columns.tolist()
        columns.remove(self.model.ID)
        if not df.empty:
            # Convert date to string according to date format
            df[self.model.DATE] = df[self.model.DATE].dt.strftime(self.model.DATE_TIME_FORMAT)
            # Convert amount to string with currency
            df[self.model.AMOUNT] = df[self.model.AMOUNT].astype(str) + " " + self.get_currency()
            # Remove ID column from dataframe
            df = df.loc[:, df.columns != self.model.ID]
            data = df.values.tolist()
        else:
            data = []

        return columns, data

    def event_transaction_changed(self, view_row, field, new_content):
        self.debug_print(f"Ctrl: Writing cell change to data base")
        self.model.edit_transaction_field(view_row, field, new_content)
        # self.view.update_data()

    def event_new_transaction(self, date, account, description, amount, category):
        self.model.new_transaction(date, account, description, amount, category)
        self.view.update_data()

    def event_selected_transaction_year_changed(self, year_str):
        self.debug_print(f"Ctrl: Selected year changed to {year_str}")
        self.selected_year = int(year_str)

    def event_selected_transaction_month_changed(self, month_str):
        self.debug_print(f"Ctrl: Selected year changed to {month_str}")
        self.selected_month = int(month_str)

    def event_open_file(self, file_path):
        self.__update_file(file_path)

        self.debug_print(f"Ctrl: File {self.file_name} loaded")

        self.model.load_from(self.file_path)
        self.view.update_data()

    def event_save_file(self, file_path=None):
        if file_path is None:
            assert self.file_path is not None, "Controller:event_save_file: Attempting to save without " \
                                           "stored or passed file_path"
            file_path = self.file_path
        self.__update_file(file_path)
        self.model.save_as(file_path)
        self.view.update_data()

    def __update_file(self, file_path):
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)

    def get_file_path(self):
        return self.file_path

    def get_loaded_file_name(self):
        return self.file_name

    def get_account_list(self):
        return self.model.get_accounts()

    def get_category_list(self):
        return self.model.get_categories()

    def get_category_name(self):
        return self.model.CATEGORY

    def get_account_name(self):
        return self.model.ACCOUNT

    def get_years_in_data(self):
        years_int = self.model.years()
        years_str = [str(year) for year in years_int]
        return years_str

    def get_months(self):
        months = [str(i) for i in range(1, 13)]
        return months

    def get_amount_name(self):
        return self.model.AMOUNT

    def get_currency(self):
        return self.model.CURRENCY
