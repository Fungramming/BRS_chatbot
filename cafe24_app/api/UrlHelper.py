# API Request URL 관리

from .DateHelper import orders_date_range
from flask import current_app
from fake_useragent import UserAgent

ua = UserAgent()

# 회원의 배송중인 주문내역을 조회하기 위한 URL(최대 3개월 이내의 주문 전체)
def get_ondelivering_orders_request_url(MallId, shop_no, member_id, AccessToken):
    start, end = orders_date_range()

    request_url = 'https://' + MallId + '.' + current_app.config['REQUEST_BASE_PATH'] + \
                  '/orders?shop_no='+ shop_no +'&start_date=' + start + '&end_date=' + end +\
                  '&member_id=' + member_id + '&date_type=order_date' + '&order_status=N00,N10,N20,N21,N22,N30&embed=items'
    headers = {'Authorization': 'Bearer' + ' ' + AccessToken, 'Content-Type': 'application/json',
               'User-Agent': ua.random}

    return request_url, headers

# 회원의 배송이 완료된 주문내역을 조회하기 위한 URL(2개씩 pagination)
def get_delivered_orders_request_url(MallId, shop_no, member_id, AccessToken, page, per_page):
    start, end = orders_date_range()

    limit = per_page + 1
    offset = ((page-1) * per_page)

    request_url = 'https://' + MallId + '.' + current_app.config['REQUEST_BASE_PATH'] + \
                  '/orders?shop_no='+ shop_no +'&start_date=' + start + '&end_date=' + end +\
                  '&member_id=' + member_id + '&date_type=order_date' + '&order_status=N40&embed=items'+\
                  '&limit=' + str(limit) + '&offset='+ str(offset)
    headers = {'Authorization': 'Bearer' + ' ' + AccessToken, 'Content-Type': 'application/json',
               'User-Agent': ua.random}

    return request_url, headers

def get_products_request_url(MallId, shop_no, AccessToken, product_num_str):
    if product_num_str == None:
        query = None
    else:
        query = '&product_no=' + product_num_str
    request_url = 'https://' + MallId + '.' + current_app.config['REQUEST_BASE_PATH'] +\
                  '/products?shop_no='+ shop_no + query
    headers = {'Authorization': 'Bearer' + ' ' + AccessToken, 'Content-Type': 'application/json',
               'User-Agent': ua.random}

    return  request_url, headers

# 회원의 아이디를 얻기위한 URL
def get_member_id_request_url(MallId, shop_no, cellphone, AccessToken):
    request_url = 'https://' + MallId + '.' + current_app.config['REQUEST_BASE_PATH'] + \
                  '/customers?shop_no='+shop_no+'&cellphone=' + cellphone
    headers = {'Authorization': 'Bearer' + ' ' + AccessToken, 'Content-Type': 'application/json',
               'User-Agent': ua.random}

    return request_url, headers

# def test_url(MallId, shop_no, member_id, AccessToken, page, per_page):
#     start, end = orders_date_range()
#
#     limit = per_page + 1
#     offset = ((page-1) * per_page)
#     print(limit)
#     print(offset)
#
#     request_url = 'https://' + MallId + '.' + current_app.config['REQUEST_BASE_PATH'] + \
#                   '/orders?shop_no='+ shop_no +'&start_date=' + start + '&end_date=' + end +\
#                   '&member_id=' + member_id + '&date_type=order_date' + '&order_status=N40&embed=items'+\
#                   '&limit=' + str(limit) + '&offset='+ str(offset)
#     headers = {'Authorization': 'Bearer' + ' ' + AccessToken, 'Content-Type': 'application/json',
#                'User-Agent': ua.random}
#
#     return request_url, headers