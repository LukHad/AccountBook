#t_Account.balance_at_date
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

acc = Account("MyAccName", 927)

acc.deposit(100, 2, dt.date(2017,12,1))
acc.withdraw(27.5, 2, dt.date(2017,12,13))
acc.deposit(100, 2, dt.date(2018,1,1))
acc.withdraw(27.5, 2, dt.date(2018,1,7))
acc.deposit(100, 2, dt.date(2018,2,1))

if acc.balance_at_date(dt.date(2018,1,6))== 1099.5:
    print("passed - Account.balance_at_date")
else:
    print("failed - Account.balance_at_date")
