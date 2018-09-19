from flask import request, app, current_app
from datetime import datetime, date
from dateutil.relativedelta import *


def orders_date_range():

    start = datetime.today() - relativedelta(months=1)
    end = datetime.today()

    start_date = start.strftime('%Y-%m-%d')
    end_date = end.strftime('%Y-%m-%d')

    return start_date, end_date
