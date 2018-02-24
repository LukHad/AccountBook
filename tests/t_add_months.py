#t_add_months
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
from util.add_months import add_months

d = dt.date(2018,3,31)

if add_months(d,-1) == dt.date(2018,2,28):
    print("passed - t_add_months - t1")
else:
    print("failed - t_add_months - t1")

if add_months(d,11) == dt.date(2019,2,28):
    print("passed - t_add_months - t2")
else:
    print("failed - t_add_months - t2")

if add_months(d,1) == dt.date(2018,4,30):
    print("passed - t_add_months - t3")
else:
    print("failed - t_add_months - t3")

if add_months(d,2) == dt.date(2018,5,31):
    print("passed - t_add_months - t4")
else:
    print("failed - t_add_months - t4")
