import datetime as dt

from Transaction import Transaction
from util.add_months import add_months

class Account:
    next_id = 1 #id 0 is reserved for "external" account
    def __init__(self, name = "Account " + str(id), init_balance = 0,
        interest_pa = 0, savings_acc = False, interest_date = dt.date.today(),
        interest_interval_months = 1, interest_categorie = ""
        ):
        self.id = Account.next_id #every new object of Account gets the next id starting at 1
        Account.next_id += 1 #increaste next_id for the next object of Account
        self.name = name
        self.init_balance = init_balance #balance at creating the account
        self.balance = init_balance #balance now
        self.transactions = []
        self.interest_pa = interest_pa #=0.01 for 1% note: negative interests are supported
        self.interest_days_in_year = 360 #europe ToDo_3
        self.interest_date = interest_date #the next date of interest payment
        self.interest_interval_months = interest_interval_months #interval of interest payments in months
        self.interest_categorie = interest_categorie
        self.savings = savings_acc #will be used to calculate percentage of savings / income

    def deposit(self, amount, date = dt.date.today(),
        categorie = "", description = "", bool_income = False
        ):
        self.balance += amount
        new_transaction = Transaction(amount, date, categorie, description, bool_income)
        self.transactions.append(new_transaction)

    def withdraw(self, amount, date = dt.date.today(),
        categorie = "", description = "", bool_income = False
        ):
        self.balance -= amount
        new_transaction = Transaction(-amount, date, categorie, description, bool_income)
        self.transactions.append(new_transaction)

    def update_interest(self):
        '''
        Calculate if an interest payment happend. Calculate the amount and create
        a transaction for each payment.
        '''
        #check if calculation is necessary
        if self.interest_pa == 0:
            return
        #start calculation
        while dt.date.today() > self.interest_date:
            #calculate daily percentage
            daily_fac = self.interest_pa / self.interest_days_in_year
            #calculate first relevant day
            i_date = self.interest_date - dt.timedelta(days=1)
            amount = 0
            #iterate through all days of current interest month to calculate
            #total monthly interest amount
            while i_date < (add_months(self.interest_date,1) - dt.timedelta(days=1)):
                amount += self.balance_at_date(i_date) * daily_fac
                i_date += dt.timedelta(days=1)
            #deposit or withdraw amount
            description = "Interest payment" #ToDo_2
            if self.interest_pa >= 0:
                self.deposit(amount,self.interest_date,self.interest_categorie,description,True)
            else:
                self.withdraw(abs(amount),self.interest_date,self.interest_categorie,description,False)
            #set new date for next interest payment
            self.interest_date = add_months(self.interest_date, self.interest_interval_months)

    def balance_at_date(self, date):
        '''
        Calculates the account balance at a certain date. The day of the date
        passed is included.
        '''
        #ToDo_4
        balance_at_date = self.init_balance
        rel_transactions = (tr for tr in self.transactions if tr.date <= date)
        for tr in rel_transactions:
            balance_at_date += tr.amount
        return balance_at_date

    def print_transactions(self):
        print(
        "ID \t"
        "Date       \t"
        "Amount \t"
        "B_Income \t"
        "Categorie \t"
        "Description \t"
        )
        for ta in self.transactions:
            print(
            str(ta.id) + "\t" +
            str(ta.date) + "\t" +
            str(ta.amount) + "\t" +
            str(ta.bool_income) + "\t\t" +
            str(ta.categorie) + "\t" +
            str(ta.description) + "\t"
            )
