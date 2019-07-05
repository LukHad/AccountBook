from datetime import datetime
import pandas as pd
import numpy as np


class TransactionBook:
    DATE = "Date"
    ACCOUNT = "Account"
    DESCRIPTION = "Description"
    AMOUNT = "Amount"
    CATEGORY = "Category"
    CURRENCY = "€"
    DATE_TIME_FORMAT = "%d.%m.%Y"
    DATE_DELIMITER = "."

    def __init__(self, path=None):
        self.path = path  # Hold the entire path to the database file including the filename
        self.accounts = []  # Holds the list of all accounts in the dataset
        self.categories = []  # Holds the list of all categories in the dataset
        # Main dataset:
        self.data = pd.DataFrame(columns=[self.DATE, self.ACCOUNT, self.DESCRIPTION, self.AMOUNT, self.CATEGORY])

    def new_transaction(self, date, account, description, amount, category):
        df = self.data
        # If its the first element in the dataset: set index to 0, else: set index to the next index available
        index = 0 if np.isnan(df.index.max()) else (df.index.max() + 1)
        # Format date string to datetime object
        date = datetime.strptime(date, self.DATE_TIME_FORMAT)
        # Add transaction to dataset
        df.loc[index] = [date, account, description, amount, category]
        self.data = df
        # Add elemets to lists if they are new
        if category not in self.categories:
            self.categories.append(category)
        if account not in self.accounts:
            self.accounts.append(account)

    def edit_transaction(self, index, date, account, description, amount, category):
        date = datetime.strptime(date, self.DATE_TIME_FORMAT)
        self.data.loc[index] = [date, account, description, amount, category]

    def delete_transaction(self, index):
        #ToDo: Implement
        pass

    def account_balance(self, account, data):
        df = data
        return df.loc[df[self.ACCOUNT] == account, self.AMOUNT].sum()

    def filter_date(self, from_date, to_date):
        data = self.data
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
        df = self.data.copy()
        df[self.DATE] = df[self.DATE].dt.strftime(self.DATE_TIME_FORMAT)
        df.to_csv(file_path, sep=';', index=False)

    def load(self):
        file_path = self.path
        self.load_from(file_path)

    def load_from(self, file_path):
        df = pd.read_csv(file_path, sep=';')
        df[self.DATE] = pd.to_datetime(df[self.DATE], format=self.DATE_TIME_FORMAT)
        self.data = df
        self.populate_lists_from_data()

# Data aggregation methods:
    def pivot_monthly_trend(self, year):
        month = 'Month'
        # Filter data for passed year
        df = self.filter_date(datetime(year, 1, 1), datetime(year, 12, 31))
        # Add additional helper column with months
        df[month] = [el.month for el in df[self.DATE]]
        # Create list with formatted months
        label = ["01.", "02.", "03.", "04.", "05.", "06.", "07.", "08.", "09.", "10.", "11.", "12."]
        label = [i + str(year) for i in label]
        # Init result list
        result = [0] * 12
        # Calculate balance at months
        for i in range(1, 13):
            result[i - 1] = df.loc[df[month] == i, self.AMOUNT].sum()
        return label, result

    def pivot_category_pie(self, df, percent=False):
        # Filter for expenses -> negative amounts only
        df = df.loc[df[self.AMOUNT] < 0]
        # Get categories which have a negative balance
        categories = df[self.CATEGORY].unique()
        categories = categories.tolist()
        # Init list of results
        result = [0] * len(categories)
        # Calculate negative sum for each category
        for i, cat in enumerate(categories):
            result[i] = df.loc[df[self.CATEGORY] == cat, self.AMOUNT].sum()
        # Sort lists ascending
        result, label = (list(t) for t in zip(*sorted(zip(result, categories))))
        # Calculate result in percent if requested
        if percent:
            sum_of_expenses = sum(result)
            for i, res in enumerate(result):
                result[i] = (res / sum_of_expenses) * 100
        return label, result
