import datetime as dt
import nose
import nose.tools
from src.model.AccountBook import AccountBook


def test_update_standing_orders(test_eng=False):
    tab = AccountBook()
    tab.new_account("Giro")
    tab.new_account("Giro2")
    tab.accounts[0].deposit(1000)

    if test_eng:
        for acc in tab.accounts:
            print(f"ID: {acc.id}; Name: {acc.name}; balance: {acc.balance}")

    tgt_acc = 2
    src_acc = 1

    tab.new_standing_order(src_acc, tgt_acc, 100, dt.date(2018, 1, 1), interval_months=1)
    tab.update_standing_orders(dt.date(2018, 2, 28))

    if test_eng:
        print("Updated standing order")
        for acc in tab.accounts:
            print(f"ID: {acc.id}; Name: {acc.name}; balance: {acc.balance}")
        print(tab.standing_orders[0].date)

    nose.tools.ok_(tab.accounts[0].balance == 800 and tab.accounts[1].balance == 200,
                   msg=f"Acc0: {tab.accounts[0].balance}, Acc1: {tab.accounts[1].balance}")


if __name__ == '__main__':
    test_update_standing_orders(test_eng=True)