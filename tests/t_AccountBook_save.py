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

tab.save()

new_AccBook = AccountBook()

new_AccBook.load("saved_data/" + tab.name)

new_AccBook.accounts[0].withdraw(100)
print(new_AccBook.accounts[0].print_transactions())
