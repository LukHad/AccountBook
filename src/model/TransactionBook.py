from datetime import datetime
import pandas as pd
import numpy as np

DATE_TIME_FORMAT = "%d.%m.%Y"


class TransactionBook:
    DATE = "Date"
    ACCOUNT = "Account"
    DESCRIPTION = "Description"
    AMOUNT = "Amount"
    CATEGORY = "Category"

    def __init__(self, path=None):
        self.path = path
        self.accounts = []
        self.categories = []
        self.data = pd.DataFrame(columns=[self.DATE, self.ACCOUNT, self.DESCRIPTION, self.AMOUNT, self.CATEGORY])

    def new_transaction(self, date, account, description, amount, category):
        df = self.data
        index = 0 if np.isnan(df.index.max()) else (df.index.max() + 1)

        date = datetime.strptime(date, DATE_TIME_FORMAT)
        df.loc[index] = [date, account, description, amount, category]
        self.data = df

    def account_balance(self, account, data):
        df = data
        return df.loc[df[self.ACCOUNT] == account, self.AMOUNT].sum()

    def filter_date(self, from_date, to_date, data):
        df = data
        df = df.loc[df[self.DATE] >= from_date]
        df = df.loc[df[self.DATE] <= to_date]
        return df

    def populate_lists_from_data(self):
        df = self.data
        categories = df[self.CATEGORY].unique()
        self.categories = categories.tolist()
        accounts = df[self.ACCOUNT].unique()
        self.accounts = accounts.tolist()

    def save(self):
        self.save_as(self.path)

    def save_as(self, file_path):
        df = self.data
        df[self.DATE] = df[self.DATE].dt.strftime(DATE_TIME_FORMAT)
        self.data.to_csv(file_path, sep=';', index=False)

    def load(self, file_path):
        df = pd.read_csv(file_path, sep=';')
        df[self.DATE] = pd.to_datetime(df[self.DATE], format=DATE_TIME_FORMAT)
        self.data = df
        self.populate_lists_from_data()
