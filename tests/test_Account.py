import datetime as dt
import nose
import nose.tools
from src.model.Account import Account


def test_account_balance_at_date():
    acc = Account("MyAccName", 927)

    acc.deposit(100, dt.date(2017, 12, 1))
    acc.withdraw(27.5, dt.date(2017, 12, 13))
    acc.deposit(100, dt.date(2018, 1, 1))
    acc.withdraw(27.5, dt.date(2018, 1, 7))
    acc.deposit(100, dt.date(2018, 2, 1))

    nose.tools.ok_(acc.balance_at_date(dt.date(2018, 1, 6)) == 1099.5, msg="Wrong balance")


def test_update_interest():
    acc = Account("MyAccName",
                  init_balance=500,
                  interest_pa=0.12,
                  interest_date = dt.date(2017, 12, 1))
    acc.deposit(1000, dt.date(2017, 12, 3), "My Income", "")
    acc.deposit(1000, dt.date(2017, 12, 20), "My Income", "")
    acc.deposit(10000, dt.date(2018, 1, 25), "My Income", "")
    acc.deposit(1500, dt.date(2018, 2, 14), "My Income", "")

    before_interest = acc.balance
    acc.update_interest(dt.date(2018, 11, 14))
    after_interest = acc.balance
    interest_amount = after_interest - before_interest
    nose.tools.ok_(interest_amount == 1543.3262847212645, msg="Wrong interest update")
