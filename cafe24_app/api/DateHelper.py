# 검색 기간 처리

from datetime import datetime
from dateutil.relativedelta import *


def orders_date_range():

    start = datetime.today() - relativedelta(months=3) + relativedelta(days=1)
    end = datetime.today()

    start_date = start.strftime('%Y-%m-%d')
    end_date = end.strftime('%Y-%m-%d')

    return start_date, end_date
