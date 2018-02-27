#t_Account.balance_at_date
#   > Account.balance_at_date
#   > Account.__init__
#   > Account.deposit
#   > Account.withdraw
#
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

acc = Account("MyAccName", 500)
acc.interest_pa = 0.12

acc.interest_date = dt.date(2017,12,1)

acc.deposit(1000, dt.date(2017,12,3), "My Income", "")
acc.deposit(1000, dt.date(2017,12,20), "My Income", "")
acc.deposit(10000, dt.date(2018,1,25), "My Income", "")
acc.deposit(1500, dt.date(2018,2,14), "My Income", "")

before_interest = acc.balance
acc.update_interest()
after_interest =acc.balance

print("Interest: " + str(after_interest-before_interest))

#acc.print_transactions()
