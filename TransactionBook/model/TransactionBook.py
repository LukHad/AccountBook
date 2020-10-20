from datetime import datetime
import pandas as pd
import numpy as np


def to_float(integer_amount):
    return integer_amount / 100.0


def to_int(float_amount):
    return int(round(float_amount * 100))


class TransactionBook:
    def __init__(self, path=""):
        # Constants ToDo: Shall be initialized from configuration file
        #   Pandas dataframe headings
        self.DATE = "Date"
        self.ACCOUNT = "Account"
        self.DESCRIPTION = "Description"
        self.AMOUNT = "Amount"
        self.CATEGORY = "Category"
        #   Other constants
        self.CURRENCY = "€"
        self.DATE_TIME_FORMAT = "%d.%m.%Y"
        self.DATE_DELIMITER = "."

        # Init data set columns:
        self._data = pd.DataFrame(columns=[self.DATE, self.ACCOUNT, self.DESCRIPTION, self.AMOUNT, self.CATEGORY])

        self.accounts = []  # Holds the list of all accounts in the dataset
        self.categories = []  # Holds the list of all categories in the dataset

    # Accessors
    def get_date_time_format(self):
        return self.DATE_TIME_FORMAT

    def get_accounts(self):
        return self.accounts

    def set_accounts(self, accounts):
        self.accounts = accounts

    def get_categories(self):
        return self.categories

    def set_categories(self, categories):
        self.categories = categories

    def get_data(self):
        return self._data.copy()

    def __set_data(self, data):
        self._data = data

    def get_account_balance(self, account):
        df = self._data
        balance = df.loc[df[self.ACCOUNT] == account, self.AMOUNT].sum()
        return to_float(balance)

    def get_total_balance(self):
        df = self._data
        total = df[self.AMOUNT].sum()
        return to_float(total)

    def add_account(self, account):
        if account not in self.accounts:
            self.accounts.append(account)
            self.accounts.sort()

    def add_category(self, category):
        if category not in self.categories:
            self.categories.append(category)
            self.categories.sort()

    def get_transaction_by_index(self, index):
        df = self.get_data()
        date = df[self.DATE].loc[index].strftime(self.DATE_TIME_FORMAT)
        account = df[self.ACCOUNT].loc[index]
        description = df[self.DESCRIPTION].loc[index]
        amount = df[self.AMOUNT].loc[index]
        category = df[self.CATEGORY].loc[index]

        return date, account, description, to_float(amount), category

    # Methods
    #   Transaction
    def new_transaction(self, date, account, description, f_amount, category):
        df = self.get_data()
        # If its the first element in the dataset: set index to 0, else: set index to the next index available
        index = 0 if np.isnan(df.index.max()) else (df.index.max() + 1)
        # Format date string to datetime object
        date = datetime.strptime(date, self.DATE_TIME_FORMAT)
        # Add transaction to dataset
        df.loc[index] = [date, account, description, to_int(f_amount), category]
        self.__set_data(df)
        # Append lists if new category or account is added to data
        self.add_category(category)
        self.add_account(account)

    def edit_transaction(self, index, date, account, description, f_amount, category):
        date = datetime.strptime(date, self.DATE_TIME_FORMAT)
        self._data.loc[index] = [date, account, description, to_int(f_amount), category]
        # Append lists if new category or account is added to data
        self.add_category(category)
        self.add_account(account)

    def edit_transaction_field(self, index, field, content):
        if field == self.DATE:
            content = datetime.strptime(content, self.DATE_TIME_FORMAT)
        elif field == self.AMOUNT:
            content = to_int(content)
        self._data[field].values[index] = content

    def delete_transaction(self, index):
        self._data = self._data.drop(index)

    def filter_date(self, from_date, to_date):
        data = self.get_data()
        df = data
        df = df.loc[df[self.DATE] >= from_date]
        df = df.loc[df[self.DATE] <= to_date]
        return df

    def populate_categories_from_data(self):
        df = self.get_data()
        categories = df[self.CATEGORY].unique()
        category_list = categories.tolist()
        category_list.sort()
        self.categories = category_list

    def populate_accounts_from_data(self):
        df = self.get_data()
        accounts = df[self.ACCOUNT].unique()
        self.accounts = accounts.tolist()

    def populate_lists_from_data(self):
        self.populate_categories_from_data()
        self.populate_accounts_from_data()

    def save_as(self, file_path):
        df = self.get_data()
        df[self.AMOUNT] = df[self.AMOUNT].apply(to_float)  # Save to csv with decimals
        df[self.DATE] = df[self.DATE].dt.strftime(self.DATE_TIME_FORMAT)  # Save with nice date format
        df.to_csv(file_path, sep=';', index=False)

    def load_from(self, file_path):
        df = pd.read_csv(file_path, sep=';')
        df[self.DATE] = pd.to_datetime(df[self.DATE], format=self.DATE_TIME_FORMAT)
        df[self.AMOUNT] = df[self.AMOUNT].apply(to_int)  # Convert decimals to integers
        self.__set_data(df)
        self.populate_lists_from_data()

    def years(self):
        df = self.get_data()
        df["Year"] = [el.year for el in df[self.DATE]]
        years = df["Year"].unique()
        return years.tolist()

    # Data aggregation methods:
    def pivot_monthly_trend(self, year, negative_amount_only=False):
        df = self.get_data()
        # Add additional helper column with months
        df["Month"] = [el.month for el in df[self.DATE]]
        df["Year"] = [el.year for el in df[self.DATE]]
        # years = df["Year"].unique()
        # years = years.tolist()
        # year = max(years)
        df = df.loc[df["Year"] == year]  # Pivot latest year of data set
        # Create list with formatted months
        label = ["01.", "02.", "03.", "04.", "05.", "06.", "07.", "08.", "09.", "10.", "11.", "12."]
        label = [i + str(year) for i in label]
        # Init result list
        result = [0] * 12
        # Calculate balance at months
        if negative_amount_only:
            df = df.loc[df[self.AMOUNT] < 0]
        for i in range(1, 13):
            i_result = df.loc[df["Month"] == i, self.AMOUNT].sum()
            result[i - 1] = to_float(i_result)
        return label, result

    def pivot_category_pie(self, df_in, percent=False):
        # Filter for expenses -> negative amounts only
        df = df_in.copy()
        df = df.loc[df[self.AMOUNT] < 0]
        # Get categories which have a negative balance
        categories = df[self.CATEGORY].unique()
        categories = categories.tolist()
        # Init list of results
        result = [0] * len(categories)
        # Calculate negative sum for each category
        for i, cat in enumerate(categories):
            i_result = df.loc[df[self.CATEGORY] == cat, self.AMOUNT].sum()
            result[i] = to_float(i_result)
        # Sort lists ascending
        result, label = (list(t) for t in zip(*sorted(zip(result, categories))))
        # Calculate result in percent if requested
        if percent:
            sum_of_expenses = sum(result)
            for i, res in enumerate(result):
                result[i] = (res / sum_of_expenses) * 100
        return label, result

    def pivot_total_balance_trend(self):
        df = self.get_data()
        # Add additional helper column with month and year
        df["Month"] = [el.month for el in df[self.DATE]]
        df["Year"] = [el.year for el in df[self.DATE]]
        # Get years and months in data
        years = df["Year"].unique()
        years = sorted(years.tolist())
        if not years:  # If dataset is empty do nothing
            return [], []
        years_min = min(years)
        years_max = max(years)

        label = []
        result = []
        for year in years:
            months = df.loc[df["Year"] == year, "Month"].unique()
            # Only pivot available data but don not leave out months with no data
            if year == years_min:
                months_start = min(months.tolist())
            else:
                months_start = 1
            if year == years_max:
                months_end = max(months.tolist())
            else:
                months_end = 12
            # Go through months of year
            for month in range(months_start, months_end + 1):
                label.append(f"{month}{self.DATE_DELIMITER}{year}")
                # calculate sum of past years and current year with past months
                integer_result = df.loc[(df["Year"] < year) | ((df["Year"] == year) & (df["Month"] <= month)),
                                        self.AMOUNT].sum()
                result.append(to_float(integer_result))

        return label, result

