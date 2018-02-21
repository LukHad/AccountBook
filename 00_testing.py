import datetime as dt

from Account import Account

acc = Account(1)

acc.deposit(540, 2, dt.date(2018,12,1), "My Income", "")
acc.deposit(23)

acc.withdraw(100)

acc.print_transactions()

print("Balance: " + str(acc.balance))
