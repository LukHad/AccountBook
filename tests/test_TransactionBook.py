from datetime import datetime
import os
import nose
import nose.tools
from TransactionBook.model.TransactionBook import *


def dummy_transactions():
    tb = TransactionBook()
    tb.new_transaction("01.07.2017", "Account 1", "My first transaction", 1000, "Income")
    tb.new_transaction("11.08.2017", "Account 1", "Cinema", -17, "Entertainment")
    tb.new_transaction("24.12.2017", "Account 2", "Bread and Milk", -5.0, "Food")
    tb.new_transaction("03.02.2018", "Account 1", "Fuel", -30, "Mobility")
    tb.new_transaction("01.12.2018", "Account 1", "Netflix", -11.95, "Entertainment")
    return tb


def dummy_transactions_2():
    tb = TransactionBook()
    tb.new_transaction("01.07.2018", "Account 1", "My first transaction", 1000, "Income")
    tb.new_transaction("11.08.2018", "Account 1", "Cinema", -17, "Entertainment")
    tb.new_transaction("24.12.2019", "Account 2", "Bread and Milk", -5.0, "Food")
    tb.new_transaction("03.02.2019", "Account 1", "Fuel", -30, "Mobility")
    tb.new_transaction("01.12.2019", "Account 1", "Netflix", -11.95, "Entertainment")
    tb.new_transaction("06.01.2019", "Account 2", "Sugar", -0.99, "Food")
    tb.new_transaction("13.05.2019", "Account 2", "Strawberries", -6.49, "Food")
    tb.new_transaction("17.09.2019", "Account 2", "Cheese", -5.0, "Food")
    return tb


def save_load(tb):
    """
    Helper function wich does save and load the data.
    :param tb: Transaction Book
    :return tb2: Transaction Book after save load operation
    """
    filename = "../tests/test_database.csv"
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
    nose.tools.ok_(tb.get_account_balance("Account 1") == 941.05, err_message)
    nose.tools.ok_(tb.get_account_balance("Account 2") == -5, err_message)


def test_filter_date(save_load_test=False):
    tb = dummy_transactions()
    if save_load_test:
        tb = save_load(tb)
        err_message = "Method test_filter_date failed after save and load"
    else:
        err_message = "Method test_filter_date failed"
    from_date = datetime.strptime("01.09.2017", tb.DATE_TIME_FORMAT)
    to_date = datetime.strptime("01.03.2018", tb.DATE_TIME_FORMAT)
    df_filtered = tb.filter_date(from_date, to_date)
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


def test_pivot_monthly_trend():
    tb = dummy_transactions()
    _, result = tb.pivot_monthly_trend(tb.get_data())

    nose.tools.ok_(result == [0, -30, 0, 0, 0, 0, 0, 0, 0, 0, 0, -11.95])


def test_pivot_category_pie():
    tb = dummy_transactions_2()
    year = 2019
    df = tb.get_data()
    df = df.loc[df[tb.DATE] >= datetime(2019, 1, 1)]
    df = df.loc[df[tb.DATE] <= datetime(2019, 12, 31)]
    cat, result = tb.pivot_category_pie(df)
    nose.tools.ok_(result == [-30, -17.48, -11.95] and cat == ['Mobility', 'Food', 'Entertainment'])


def test_years():
    tb = dummy_transactions()
    nose.tools.ok_(tb.years() == [2017, 2018])


def test_total_balance():
    tb = dummy_transactions()
    nose.tools.ok_(tb.get_total_balance() == 936.05)


def test_delete_transaction():
    tb = dummy_transactions()
    nose.tools.ok_(tb.get_total_balance() == 936.05)
    tb.delete_transaction(2)
    nose.tools.ok_(tb.get_total_balance() == 941.05)
    tb.delete_transaction(1)
    nose.tools.ok_(tb.get_total_balance() == 958.05)


def test_edit_transaction_field():
    tb = dummy_transactions()
    # Test amount
    tb.edit_transaction_field(3, tb.AMOUNT, -50)
    nose.tools.ok_(tb.get_total_balance() == 916.05)

    # Test description
    new_description = "Movies and Popcorn"
    df_num = 1
    tb.edit_transaction_field(df_num, tb.DESCRIPTION, new_description)
    df = tb.get_data()
    nose.tools.ok_(df[tb.DESCRIPTION].values[df_num] == new_description)


def test_get_transaction_by_index():
    tb = dummy_transactions_2()
    date, account, description, amount, category = tb.get_transaction_by_index(2)
    nose.tools.ok_(date == "24.12.2019" and
                   account == "Account 2" and
                   description == "Bread and Milk" and
                   amount == -5.0 and
                   category == "Food")


def test_add_account():
    tb = dummy_transactions_2()
    tb.add_account("Depot")
    nose.tools.ok_(tb.get_accounts() == ['Account 1', 'Account 2', 'Depot'])


def test_add_category():
    tb = dummy_transactions_2()
    expected_categories = tb.get_categories()
    expected_categories.append("Sport")
    tb.add_category("Sport")
    nose.tools.ok_(tb.get_categories() == expected_categories)


if __name__ == '__main__':
    test_populate_list_from_data()
    test_filter_date()
    test_account_balance()
    test_save_load()
    test_pivot_category_pie()
    test_years()
    test_total_balance()
    test_pivot_monthly_trend()
    test_delete_transaction()
    test_edit_transaction_field()
    test_add_account()
    test_add_category()
