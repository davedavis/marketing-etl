from datetime import timedelta, date
from dateutil import relativedelta

NEXT_MONDAY = relativedelta.relativedelta(weekday=relativedelta.MO)
LAST_MONDAY = relativedelta.relativedelta(weekday=relativedelta.MO(-1))
ONE_WEEK = timedelta(weeks=1)


# def get_week_in_quarter(dt: datetime) -> typing.Tuple[int, int, int]:
def get_week_in_quarter(dt):
    d: date = dt.date()
    year = d.year

    # Q0 = January 1, Q1 = April 1, Q2 = July 1, Q3 = October 1
    quarter = ((d.month - 1) // 3)
    quarter_start = date(year, (quarter * 3) + 1, 1)
    quarter_week_2_monday = quarter_start + NEXT_MONDAY

    if d < quarter_week_2_monday:
        week = 1
    else:
        cur_week_monday = d + LAST_MONDAY
        week = int((cur_week_monday - quarter_week_2_monday) / ONE_WEEK) + 2

    if quarter == 0:
        year -= 1
        quarter = 4

    return week
