# 배송 조회를 위한 API

import requests
from . import api
from cafe24_app.api.AceessTokenHelper import *
from .UrlHelper import *
from flask import request, jsonify, current_app
from ..models import Scripttags


# 회원의 1개월간 배송안된 모든 주문 상품을 조회하기위한 API
@api.route('/tracking/')
def get_orders():
    mall_id = request.args.get('mall_id')
    shop_no = request.args.get('shop_no')
    member_id = request.args.get('member_id')

    orders_list = list()
    orders_status = {'N00': '입급전', 'N10': '상품 준비중', 'N20': '배송 준비중', 'N21': '배송대기', 'N22': '배송보류', 'N30': '배송중'}
    product_num_list = list()
    product_image_list = dict()

    MallId, AccessToken = Confirm_access_expiration(mall_id, shop_no)
    request_url, headers = get_orders_request_url(MallId, member_id, AccessToken)
    response = requests.get(request_url, headers=headers)
    orders = response.json()['orders']

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

# 회원의 특정 상품의 배송 상태를 조회하기 위한 API
# @api.route('/tracking/item/')
# def specific_shipping_status():
#     mall_id = request.args.get('mall_id')
#     script_no = request.args.get('script_no')
#     member_id = request.args.get('member_id')
#     order_id = request.args.get('order_id')
#     shop_no = Scripttags.query.filter_by(mall_id=mall_id).filter_by(script_no=script_no).first().shop_no
#
#     MallId, AccessToken = Confirm_access_expiration(mall_id, shop_no)
#
#     request_url, headers = specific_shipping_status_request_url(MallId, member_id, order_id, AccessToken)
#
#     response = requests.get(request_url, headers=headers)
#     result = response.json()
#
#     return jsonify(result)

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