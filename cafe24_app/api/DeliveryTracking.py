# 배송 조회를 위한 API

import requests
from . import api
from cafe24_app.api.AceessTokenHelper import *
from .UrlHelper import *
from flask import request, jsonify, current_app
from ..models import Scripttags


# 회원의 3개월간 배송안된 모든 주문 상품을 조회하기위한 API
@api.route('/ondelivering/')
def get_orders_delivering():
    mall_id = request.args.get('mall_id')
    shop_no = request.args.get('shop_no')
    member_id = request.args.get('member_id')

    orders_list = list()
    orders_status = {'N00': '입급전', 'N10': '상품 준비중', 'N20': '배송 준비중', 'N21': '배송대기', 'N22': '배송보류', 'N30': '배송중'}
    orders_status_code = 'N00,N10,N20,N21,N22,N30'
    product_num_list = list()
    product_image_list = dict()

    MallId, AccessToken = Confirm_access_expiration(mall_id, shop_no)
    request_url, headers = get_orders_request_url(MallId, member_id, AccessToken, orders_status_code)
    response = requests.get(request_url, headers=headers)
    orders = response.json()['orders']

    if len(orders) == 0:
        return jsonify({'orders': '배송상태에 있는 주문이 없습니다.'})

    for order in orders:
        request_url, headers = get_orders_items_request_url(MallId, order['order_id'], AccessToken)
        response = requests.get(request_url, headers=headers)
        items = response.json()['items']

        for item in items:
            product_num_list.append(item['product_no'])
            if item['order_status'] == 'N40':
                pass
            else:
                item['order_id'] = order['order_id']
                item['order_status_message'] = orders_status[item['order_status']]
                orders_list.append(item)

    product_num_str = ','.join(str(n) for n in set(product_num_list))
    request_url, headers =  get_products_request_url(MallId, AccessToken, product_num_str)
    response = requests.get(request_url, headers=headers)
    products = response.json()['products']

    for product in products:
        product_image_list[int(product['product_no'])] = {'detail_image': product['detail_image'],
                                                          'list_image': product['list_image'],
                                                          'small_image': product['small_image'],
                                                          'tiny_image': product['tiny_image']}
    for order in orders_list:
        order['image_url'] = product_image_list[int(order['product_no'])]

    return jsonify({'orders': orders_list})

# 회원의 3개월간 배송이 완료된 배송 상태를 조회하기 위한 API
@api.route('/delivered/')
def get_orders_delivered():
    mall_id = request.args.get('mall_id')
    shop_no = request.args.get('shop_no')
    member_id = request.args.get('member_id')

    orders_list = list()
    orders_status = {'N40': '배송완료'}
    orders_status_code = 'N40'
    product_num_list = list()
    product_image_list = dict()

    MallId, AccessToken = Confirm_access_expiration(mall_id, shop_no)
    request_url, headers = get_orders_request_url(MallId, member_id, AccessToken, orders_status_code)
    response = requests.get(request_url, headers=headers)
    orders = response.json()['orders']

    if len(orders) == 0:
        return jsonify({'orders': '배송완료된 주문이 없습니다.'})

    for order in orders:
        request_url, headers = get_orders_items_request_url(MallId, order['order_id'], AccessToken)
        response = requests.get(request_url, headers=headers)
        items = response.json()['items']

        for item in items:
            product_num_list.append(item['product_no'])
            if item['order_status'] != 'N40':
                pass
            else:
                item['order_id'] = order['order_id']
                item['order_status_message'] = orders_status[item['order_status']]
                orders_list.append(item)

    product_num_str = ','.join(str(n) for n in set(product_num_list))
    request_url, headers =  get_products_request_url(MallId, AccessToken, product_num_str)
    response = requests.get(request_url, headers=headers)
    products = response.json()['products']

    for product in products:
        product_image_list[int(product['product_no'])] = {'detail_image': product['detail_image'],
                                                          'list_image': product['list_image'],
                                                          'small_image': product['small_image'],
                                                          'tiny_image': product['tiny_image']}
    for order in orders_list:
        order['image_url'] = product_image_list[int(order['product_no'])]

    return jsonify({'orders': orders_list})

#전화번호를 이용하여 회원의 아이디를 얻기 위한 API
@api.route('/user/')
def get_member_id():
    mall_id = request.args.get('mall_id')
    script_no = request.args.get('script_no')
    cellphone = request.args.get('cellphone')
    shop_no = Scripttags.query.filter_by(mall_id=mall_id).filter_by(script_no=script_no).first().shop_no

    MallId, AccessToken = Confirm_access_expiration(mall_id, shop_no)

    request_url, headers = get_member_id_request_url(MallId, cellphone, AccessToken)

    response = requests.get(request_url, headers=headers)
    result = response.json()

    return jsonify(result)

# # test하기 위한 API
# @api.route('/test/')
# def test():
#     mall_id = request.args.get('mall_id')
#     script_no = request.args.get('script_no')
#     shop_no = Scripttags.query.filter_by(mall_id=mall_id).filter_by(script_no=script_no).first().shop_no
#
#     MallId, AccessToken = Confirm_access_expiration(mall_id, shop_no)
#
#     request_url = 'https://' + MallId + '.' + current_app.config['REQUEST_BASE_PATH']+'/products'
#     headers = {'Authorization': 'Bearer'+ ' ' + AccessToken, 'Content-Type': 'application/json'}
#
#     response = requests.get(request_url, headers=headers)
#     result = response.json()
#
#     return jsonify(result)