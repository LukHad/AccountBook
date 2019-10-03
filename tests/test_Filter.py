import os
import nose
import nose.tools
from TransactionBook.model.Filter import *
from tests.test_TransactionBook import dummy_transactions_2
from datetime import datetime


def test_filter():
    tb = dummy_transactions_2()
    print(tb.get_data())
    my_filter = Filter()
   # my_filter.select(tb.CATEGORY, "Food")
   # my_filter.select(tb.CATEGORY, "Income")
   # my_filter.select(tb.CATEGORY, "Income")

    from_date = datetime.strptime("01.01.2019", tb.DATE_TIME_FORMAT)
    to_date = datetime.strptime("30.07.2019", tb.DATE_TIME_FORMAT)

    my_filter.select_date_range(tb.DATE, from_date, to_date)
    my_filter.deselect_date_range(tb.DATE)
    print(my_filter.filter_date_time)
    print(f"Result: {my_filter.filter(tb.get_data())}")

    print(my_filter.check_if_selected(tb.CATEGORY, ["Income", "Blub", "Food", "Blob"]))


if __name__ == '__main__':
    test_filter()