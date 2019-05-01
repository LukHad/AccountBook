import datetime as dt
import nose
import nose.tools
from src.model.AccountBook import AccountBook


def test_update_standing_orders():
    tab = AccountBook()
    tab.new_account("Giro")
    tab.new_account("Giro2")
    tab.accounts[0].deposit(1000)

    tgt_acc = tab.accounts[1].id
    src_acc = tab.accounts[0].id

    tab.new_standing_order(src_acc, tgt_acc, 100, dt.date(2018, 1, 1), interval_months=1)
    tab.update_standing_orders(dt.date(2018, 2, 28))

    nose.tools.ok_(tab.accounts[0].balance == 800 and tab.accounts[1].balance == 200,
                   msg=f"Acc0: {tab.accounts[0].balance}, Acc1: {tab.accounts[1].balance}")


def test_get_acc_array_pos():
    tab = AccountBook()
    tab.new_account("Acc_1")
    tab.new_account("Acc_2")
    nose.tools.ok_(tab.get_acc_array_pos(9999) is None, "Assert_1")


if __name__ == '__main__':
    test_update_standing_orders()
    test_get_acc_array_pos()
