import datetime as dt
from Account import Account
from Categorie import Categorie
from StandingOrder import StandingOrder

class AccountBook:
    def __init__(self):
        self.accounts = []
        self.categories = []
        self.standing_orders = []

    #def update(self):
        #start with standing standing_orders
        #now update_interest of all accounts

    def new_account(self, *args):
        self.accounts.append(Account(*args))

    def new_categorie(self, *args):
        self.categories.append(Account(*args))

    def new_standing_order(self, *args):
        self.standing_orders.append(Account(*args))

    def get_acc_array_pos(self, acc_id):
        for i, acc in enumerate(self.accounts):
            if acc.id == acc_id:
                return i
        return -1 #not found
