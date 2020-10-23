import os
from datetime import datetime

from TransactionBook.gui.MainWindow import MainWindow
from TransactionBook.model.TransactionBook import TransactionBook, to_float


class Controller:
    def __init__(self):
        self.DEBUG = True
        self.file_path = r"C:\Users\Win10VM\Documents\MyLocalFiles\Python_Projects\TransactionBook\util\dummy_database.csv" # ToDo: Test, remove
        self.file_name_for_title = "Transaction Book"
        self.selected_year = None
        self.selected_month = None
        self.view_table_model_map = []  # [3] = 5 : 3 view table index, 5 is model df index
        self.model = TransactionBook()
        self.view = MainWindow(self)

        self.initialize()

    def initialize(self):
        self.view.update_data()  # initialize view
        today = datetime.today()
        # Select current month
        self.view.set_selected_month(today.month)
        self.selected_month = today.month

        if self.file_path is not None:
            self.__update_file(self.file_path)
            self.model.load_from(self.file_path)
            # Select most recent year in database
            latest_year_in_data = int(self.get_years_in_data_as_str()[0])
            self.view.set_selected_year(latest_year_in_data)
            self.selected_year = latest_year_in_data

        self.view.update_data()  # update view

    def debug_print(self, text):
        if self.DEBUG:
            print(text)

    def get_account_data(self):
        accounts = self.model.get_accounts()
        acc_data = {}
        for acc in accounts:
            acc_data[acc] = self.model.get_account_balance(acc)

        return acc_data

    def get_total_balance_trend(self):
        label, result = self.model.pivot_total_balance_trend()
        return label, result

    def get_monthly_bar_trend(self):
        label, result = self.model.pivot_monthly_trend(self.selected_year)  # ToDo: selected year is only temporary. Plot shall have its own year filter
        return label, result

    def get_pretty_amount_str(self, amount):
        amount_str = "{:.2f}".format(amount)
        currency_str = self.get_currency()
        return amount_str + " " + currency_str

    def get_transaction_table_data(self):
        df = self.model.get_data()
        columns = df.columns.tolist()
        if not df.empty:
            # Filter selected month and date
            month = "Month"
            year = "Year"
            df[month] = [el.month for el in df[self.model.DATE]]
            df[year] = [el.year for el in df[self.model.DATE]]
            self.debug_print(f"Ctrl: Filtering data for year {self.selected_year} and month {self.selected_month}")
            df = df.loc[df[month] == self.selected_month]
            df = df.loc[df[year] == self.selected_year]
            # Sort data by date
            df = df.sort_values(by=self.model.DATE)
            # Convert date to string according to date format
            df[self.model.DATE] = df[self.model.DATE].dt.strftime(self.model.DATE_TIME_FORMAT)
            # Convert amount to string with currency
            df[self.model.AMOUNT] = df[self.model.AMOUNT].apply(to_float)
            # df[self.model.AMOUNT] = df[self.model.AMOUNT].astype(str) + " " + self.get_currency()
            # Remove Month and Year column
            df = df.loc[:, df.columns != month]
            df = df.loc[:, df.columns != year]

            self.view_table_model_map = df.index.tolist()  # Save a map to know which model data corresponds to the displayed data
            data = df.values.tolist()
        else:
            self.view_table_model_map = []
            data = []

        return columns, data

    def event_new_transaction(self, date, account, description, amount, category):
        self.debug_print(f"Ctrl: New transaction: [{date}, {account}, {description}, {amount}, {category}]")
        self.model.new_transaction(date, account, description, amount, category)

        if '*' not in self.file_name_for_title:
            self.file_name_for_title = "*" + self.file_name_for_title
        self.view.update_data()

    def event_edit_transaction(self, view_id, date, account, description, amount, category):
        model_index = self.view_table_model_map[view_id]
        self.debug_print(f"Ctrl: Edit transaction (view={view_id}, model={model_index}): "
                         f"[{date}, {account}, {description}, {amount}, {category}]")
        self.model.edit_transaction(model_index, date, account, description, amount, category)

        if '*' not in self.file_name_for_title:
            self.file_name_for_title = "*" + self.file_name_for_title
        self.view.update_data()

    def event_delete_transaction(self, view_id_list):
        for view_id in view_id_list:
            model_index = self.view_table_model_map[view_id]
            self.debug_print(f"Ctrl: Deleting (view={view_id}, model={model_index})")
            self.model.delete_transaction(model_index)

        if '*' not in self.file_name_for_title:
            self.file_name_for_title = "*" + self.file_name_for_title
        self.view.update_data()

    def event_selected_transaction_year_changed(self, year_str):
        self.debug_print(f"Ctrl: Selected year changed to {year_str}")
        self.selected_year = int(year_str)
        self.view.update_data()

    def event_selected_transaction_month_changed(self, month_str):
        self.debug_print(f"Ctrl: Selected month changed to {month_str}")
        self.selected_month = int(month_str)
        self.view.update_data()

    def event_open_file(self, file_path):
        self.__update_file(file_path)
        self.debug_print(f"Ctrl: File {self.file_name_for_title} loaded")

        self.initialize()

    def event_save_file(self, file_path=None):
        if file_path is None:
            assert self.file_path is not None, "Controller:event_save_file: Attempting to save without " \
                                           "stored or passed file_path"
            file_path = self.file_path
        self.__update_file(file_path)
        self.model.save_as(file_path)
        self.view.update_data()

    def event_add_category(self, category):
        self.debug_print(f"Ctrl: Adding Category {category} to model")
        self.model.add_category(category)

    def event_add_account(self, account):
        self.debug_print(f"Ctrl: Adding Account {account} to model")
        self.model.add_account(account)

    def __update_file(self, file_path):
        self.file_path = file_path
        self.file_name_for_title = os.path.basename(file_path)

    def get_file_path(self):
        return self.file_path

    def get_transaction_from_view_id(self, view_id):
        model_index = self.view_table_model_map[view_id]
        date, account, description, amount, category = self.model.get_transaction_by_index(model_index)
        return date, account, description, amount, category

    def get_loaded_file_name_for_title(self):
        return self.file_name_for_title

    def get_account_list(self):
        return self.model.get_accounts()

    def get_category_list(self):
        return self.model.get_categories()

    def get_years_in_data_as_str(self):
        years_int = self.model.years()
        years_int = sorted(years_int, reverse=True)
        years_str = [str(year) for year in years_int]
        return years_str

    def get_months_as_str(self):
        months_str = [str(i) for i in range(1, 13)]
        return months_str

    def get_date_time_format(self):
        return 'dd.MM.yyyy'  # ToDo: Implement mapping between model format and QtCore.QtDate.troString format

    def get_amount_name(self):
        return self.model.AMOUNT

    def get_currency(self):
        return self.model.CURRENCY
