#add src directory to path
import sys
import os.path
act_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.abspath(os.path.join(act_dir, os.pardir))
src_dir = os.path.join(parent_dir, "src")
sys.path.append(src_dir)
#
import datetime as dt
#
from Account import Account

acc = Account("MyAccName", 900)
acc2 = Account("MyAccName2", 0)

acc.interest_pa = 0.12
acc.interest_date = dt.date(2018,2,10)

acc.deposit(100, dt.date(2017,12,1), "My Income", "")
acc.deposit(100, dt.date(2018,1,1), "My Income", "")
acc2.deposit(100, dt.date(2018,2,1), "My Income in acc2", "")
acc.deposit(100, dt.date(2018,2,1), "My Income", "")
acc.withdraw(100, dt.date(2018,2,1), "My Income", "")

acc.update_interest()

acc.print_transactions()

print("")
print("Balance: " + str(acc.balance))
print("Next interest payment: " + str(acc.interest_date))
print("Balance 2018-01-10: " + str(acc.balance_at_date(dt.date(1018,1,10))))
