from random import choice
from datetime import datetime, timedelta


def generate_status(order_status ,order_date):


    if order_status == 'N00':
        paid = 'F'
        payment_date = None
        status_code = choice(['C1', 'N1'])
        if status_code == 'C1':
            cancel_date = order_date + timedelta(hours=1)
        else:
            cancel_date = None
        shipping_status = 'F'
        tracking_no = None
        shipping_code = None
        shipped_date = None
        delivered_date = None
        return_request_date = None
        return_date = None
        cancel_request_date = None
        refund_date = None
        exchange_request_date = None
        exchange_date = None

    status = {'paid': paid,
              'payment_date': payment_date,
              'status_code' : status_code,
              'cancel_date': cancel_date,
              'shipping_status': shipping_status,
              'tracking_no': tracking_no,
              'shipping_code': shipping_code,
              'shipped_date': shipped_date,
              'delivered_date': delivered_date,
              'return_request_date': return_request_date,
              'return_date': return_date,
              'cancel_request_date': cancel_request_date,
              'refund_date': refund_date,
              'exchange_request_date': exchange_request_date,
              'exchange_date': exchange_date}
    return status