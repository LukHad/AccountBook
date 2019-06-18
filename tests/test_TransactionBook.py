from datetime import datetime
import os
import nose
import nose.tools
from src.model.TransactionBook import *


def dummy_transactions():
    tb = TransactionBook()
    tb.new_transaction("01.07.2017", "Account 1", "My first transaction", 1000, "Income")
    tb.new_transaction("11.08.2017", "Account 1", "Cinema", -17, "Entertainment")
    tb.new_transaction("24.12.2017", "Account 2", "Bread and Milk", -5.0, "Food")
    tb.new_transaction("03.02.2018", "Account 1", "Fuel", -30, "Mobility")
    tb.new_transaction("01.12.2018", "Account 1", "Netflix", -11.95, "Entertainment")
    return tb


def save_load(tb):
    """
    Helper function wich does save and load the data.
    :param tb: Transaction Book
    :return tb2: Transaction Book after save load operation
    """
    filename = "dummy_database.csv"
    tb.save_as(filename)
    tb2 = TransactionBook()
    tb2.load_from(filename)
    os.remove(filename)
    return tb2


def test_account_balance(save_load_test=False):
    tb = dummy_transactions()
    if save_load_test:
        tb = save_load(tb)
        err_message = "Method account_balance failed after save and load"
    else:
        err_message = "Method account_balance failed"
    nose.tools.ok_(tb.account_balance("Account 1", tb.data) == 941.05, err_message)
    nose.tools.ok_(tb.account_balance("Account 2", tb.data) == -5, err_message)


def test_filter_date(save_load_test=False):
    tb = dummy_transactions()
    if save_load_test:
        tb = save_load(tb)
        err_message = "Method test_filter_date failed after save and load"
    else:
        err_message = "Method test_filter_date failed"
    from_date = datetime.strptime("01.09.2017", tb.DATE_TIME_FORMAT)
    to_date = datetime.strptime("01.03.2018", tb.DATE_TIME_FORMAT)
    df_filtered = tb.filter_date(from_date, to_date, tb.data)
    df_filtered = df_filtered.reset_index()

    ass_cond = (df_filtered[tb.DATE][0] == datetime.strptime("24.12.2017", tb.DATE_TIME_FORMAT) and
                df_filtered[tb.DATE][1] == datetime.strptime("03.02.2018", tb.DATE_TIME_FORMAT))

    nose.tools.ok_(ass_cond, err_message)


def test_save_load():
    test_filter_date(True)
    test_account_balance(True)


def test_populate_list_from_data():
    tb = dummy_transactions()
    tb.populate_lists_from_data()

    exp_cat = ['Income', 'Entertainment', 'Food', 'Mobility']
    exp_acc = ['Account 1', 'Account 2']
    ass_cond_cat = all(x in tb.categories for x in exp_cat) and (len(tb.categories) == len(exp_cat))
    ass_cond_acc = all(x in tb.accounts for x in exp_acc) and (len(tb.accounts) == len(exp_acc))

    nose.tools.ok_(ass_cond_cat and ass_cond_acc, "populate_lists_from_data failed")


if __name__ == '__main__':
    test_populate_list_from_data()
    test_filter_date()
    test_account_balance()
    test_save_load()
