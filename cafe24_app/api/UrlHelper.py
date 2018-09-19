# API Request URL 관리

from .DateHelper import orders_date_range
from flask import current_app
from ..helper import random_str
from urllib.parse import urlencode
from base64 import b64encode

# 회원의 주문내역을 조회하기 위한 URL(최대 1개원 이내의 주문)
def get_order_request_url(MallId, member_id, AccessToken):
    start, end = orders_date_range()

    request_url = 'https://' + MallId + '.' + current_app.config['REQUEST_BASE_PATH'] + \
                  '/orders?start_date=' + start + '&end_date=' + end + '&member_id=' + member_id + '&date_type=order_date'
    headers = {'Authorization': 'Bearer' + ' ' + AccessToken, 'Content-Type': 'application/json'}

    return request_url, headers

# 회원의 특정 상품의 배송 상태를 조회하기 위한 URL
def specific_shipping_status_request_url(MallId, member_id, order_id, AccessToken):
    start, end = orders_date_range()

    request_url = 'https://' + MallId + '.' + current_app.config['REQUEST_BASE_PATH'] + \
                  '/orders?start_date=' + start + '&end_date=' + end + '&member_id=' + member_id + '&order_id=' + order_id + '&date_type=order_date'
    headers = {'Authorization': 'Bearer' + ' ' + AccessToken, 'Content-Type': 'application/json'}

    return request_url, headers

# 회원의 아이디를 얻기위한 URL
def get_member_id_request_url(MallId, cellphone, AccessToken):
    request_url = 'https://' + MallId + '.' + current_app.config[
        'REQUEST_BASE_PATH'] + '/customers?cellphone=' + cellphone
    headers = {'Authorization': 'Bearer' + ' ' + AccessToken, 'Content-Type': 'application/json'}

    return request_url, headers