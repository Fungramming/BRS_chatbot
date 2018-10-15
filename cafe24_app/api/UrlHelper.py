# API Request URL 관리

from .DateHelper import orders_date_range
from flask import current_app
from fake_useragent import UserAgent

ua = UserAgent()

# 회원의 주문내역을 조회하기 위한 URL(최대 1개원 이내의 주문)
def get_orders_request_url(MallId, member_id, AccessToken, orders_status_code):
    start, end = orders_date_range()

    request_url = 'https://' + MallId + '.' + current_app.config['REQUEST_BASE_PATH'] + \
                  '/orders?start_date=' + start + '&end_date=' + end + '&member_id=' + member_id + '&date_type=order_date' + '&order_status=' + orders_status_code + '&limit=500'
    headers = {'Authorization': 'Bearer' + ' ' + AccessToken, 'Content-Type': 'application/json',
               'User-Agent': ua.random}

    return request_url, headers

# 회원의 특정 주문의 배송 상태를 조회하기 위한 URL
def get_orders_items_request_url(MallId, order_id, AccessToken):
    start, end = orders_date_range()

    request_url = 'https://' + MallId + '.' + current_app.config['REQUEST_BASE_PATH'] + '/orders/' + order_id + '/items'
    headers = {'Authorization': 'Bearer' + ' ' + AccessToken, 'Content-Type': 'application/json',
               'User-Agent': ua.random}

    return request_url, headers

def get_products_request_url(MallId, AccessToken, product_num_str):
    if product_num_str == None:
        query = None
    else:
        query = '?product_no=' + product_num_str
    request_url = 'https://' + MallId + '.' + current_app.config['REQUEST_BASE_PATH'] + '/products' + query
    headers = {'Authorization': 'Bearer' + ' ' + AccessToken, 'Content-Type': 'application/json',
               'User-Agent': ua.random}

    return  request_url, headers

# 회원의 아이디를 얻기위한 URL
def get_member_id_request_url(MallId, cellphone, AccessToken):
    request_url = 'https://' + MallId + '.' + current_app.config['REQUEST_BASE_PATH'] + '/customers?cellphone=' + cellphone
    headers = {'Authorization': 'Bearer' + ' ' + AccessToken, 'Content-Type': 'application/json',
               'User-Agent': ua.random}

    return request_url, headers