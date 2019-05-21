from src.model.AccountBook import AccountBook


class Adapter:
    def __init__(self):
        self.acc_book = AccountBook()

    def req_acc_list(self):
        """
        Get list of account names
        :return: list of account names
        """
        acc_list = [acc.name for acc in self.acc_book.accounts]
        return acc_list

    def req_cat_list(self):
        """
        Get list of categories
        :return: list of categories names
        """
        return ["Income", "Rent", "Holidays", "Presents", "Sports and Health", "Food and Drinks", "Cinema"]

    def push_new_account(self, name, balance, currency, interest):
        self.acc_book.new_account(name=name, balance=balance, currency=currency, interest=interest)

    def save(self):
        self.acc_book.save()
        print("save model")

    def load(self):
        #self.acc_book.load()
        print("load model")
