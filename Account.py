import datetime as dt

from Transaction import Transaction

class Account:
    def __init__(self, id, name = "Account " + str(id),
        interest_pa = 0, savings_acc = False, interest_date = dt.date.today(),
        interest_interval_months = 1
        ):
        self.id = id
        self.name = name
        self.balance = 0
        self.transactions = []
        self.last_transaction_id = 0 #to never create to transactions with the same id in the same acc
        self.standing_orders = []
        self.interest_pa = interest_pa
        self.interest_date = interest_date
        self.interest_interval_months = interest_interval_months
        self.savings = savings_acc

    def deposit(self, amount, src_acc_id = 0, categorie = "", description = "",
        date = dt.date.today(), bool_income = True
        ):
        self.balance += amount
        #create transaction
        nt_id = self.last_transaction_id + 1
        tgt_id = self.id
        new_transaction = Transaction(nt_id, src_acc_id, tgt_id, amount, date, categorie, description, bool_income)
        #add transaction to transaction list
        self.transactions.append(new_transaction)

    def print_transactions(self):
        print(
        "ID \t"
        "Date       \t"
        "Amount \t"
        "Src \t"
        "Target \t"
        "B_Income \t"
        "Categorie \t"
        "Description \t"
        )
        for ta in self.transactions:
            print(
            str(ta.id) + "\t" +
            str(ta.date) + "\t" +
            str(ta.amount) + "\t" +
            str(ta.src_acc_id) + "\t" +
            str(ta.target_acc_id) + "\t" +
            str(ta.bool_income) + "\t" +
            str(ta.categorie) + "\t" +
            str(ta.description) + "\t"
            )
