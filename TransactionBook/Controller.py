

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Test
        self.model.load_from(r"C:\Users\Win10VM\Documents\MyLocalFiles\Python_Projects\TransactionBook\tests\dummy_database.csv")
        # End Test
        self.populate_transaction_view()

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