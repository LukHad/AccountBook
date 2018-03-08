import sys
import os.path
import datetime as dt
# add src directory to path
act_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.abspath(os.path.join(act_dir, os.pardir))
src_dir = os.path.join(parent_dir, "src")
sys.path.append(src_dir)
from AccountBook import AccountBook

tab = AccountBook()

tab.new_account("Giro")
tab.new_account("Giro2")

tab.accounts[0].deposit(1000)

print(tab.accounts[0].balance)
print(tab.accounts[1].balance)
tgt_acc = 2
src_acc = 1
tab.new_standing_order(src_acc, tgt_acc, 100, dt.date(2018, 1, 3))
tab.new_standing_order(tgt_acc, src_acc, 10, dt.date(2018, 2, 3))

tab.update_standing_orders()

print(tab.accounts[0].balance)
print(tab.accounts[1].balance)
