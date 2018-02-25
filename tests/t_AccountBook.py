#add src directory to path
import sys
import os.path
act_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.abspath(os.path.join(act_dir, os.pardir))
src_dir = os.path.join(parent_dir, "src")
sys.path.append(src_dir)
#
from AccountBook import AccountBook

tab = AccountBook()

tab.new_account("Giro")

id_ = tab.get_acc_array_pos(1)
