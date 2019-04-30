# t_add_months
#
# add src directory to path
import nose
import nose.tools
import datetime as dt
from src.model.util.add_months import add_months


def test_add_months():
    d = dt.date(2018, 3, 31)
    nose.tools.ok_(add_months(d, -1) == dt.date(2018, 2, 28))
    nose.tools.ok_(add_months(d, 11) == dt.date(2019, 2, 28))
    nose.tools.ok_(add_months(d,  1) == dt.date(2018, 4, 30))
    nose.tools.ok_(add_months(d,  2) == dt.date(2018, 5, 31))
