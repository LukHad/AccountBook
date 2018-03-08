import datetime
import calendar


def add_months(date, months):
    '''
    Adds (or substracts for negative months) a number of months to a date.
    Does round down if there are less days inthe next month.
    '''
    month = date.month - 1 + months
    year = date.year + month // 12
    month = month % 12 + 1
    day = min(date.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)
