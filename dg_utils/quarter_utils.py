from datetime import datetime

from datequarter import DateQuarter


def get_quarter_from_date(date):
    """Takes a date object and returns the fiscal quarter of that date.
        Args:
            date (date): The date to get the quarter of.
    """

    # This setup currently returns the quarter with the fiscal year starting in April.
    # ToDo: Make this more generic.
    quarter = DateQuarter.from_date(date).quarter()
    if quarter == 1:
        return 4
    else:
        return quarter - 1


def get_start_of_quarter(date):
    start_of_quarter = DateQuarter.from_date(date).start_date()
    return start_of_quarter


print(get_start_of_quarter(datetime.now()))
