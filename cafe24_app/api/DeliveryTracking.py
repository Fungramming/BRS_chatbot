# 배송 조회를 위한 API

import requests
from . import api
from cafe24_app.api.AceessTokenHelper import *
from .UrlHelper import *
from flask import request, jsonify, current_app, url_for


# 회원의 3개월간 배송안된 모든 주문 상품을 조회하기위한 API
@api.route('/ondelivering/')
def get_orders_delivering():
    print(request)
    src_name = request.args.get('src_name')
    member_id = request.args.get('member_id')

    # accesstoken 확인 절차 및 주문조회
    mall_id, shop_no = get_mallid_shopno(src_name, 0)
    MallId, AccessToken = Confirm_access_expiration(mall_id, shop_no)
    request_url, headers = get_ondelivering_orders_request_url(MallId, shop_no, member_id, AccessToken)
    response = requests.get(request_url, headers=headers)
    result = response.json()

    if 'error' in result:
        return jsonify({'error': result['error']})

    orders = result['orders']

    if len(orders) == 0:
        return jsonify({'orders': '배송상태에 있는 주문이 없습니다.'})

    orders_list, product_no_list, product_image_list = list(), list(), dict()

    # data 가공처리중(product image 조회를 위한 작업도 동시에 진행)
    for order in orders:
        items = order['items']
        item_list = list()

        for item in items:
            item_json = {'order_item_code': item['order_item_code'],
                         'order_status': item['order_status'],
                         'product_code': item['product_code'],
                         'product_name': item['product_name'],
                         'product_no': item['product_no'],
                         'product_price': item['product_price'],
                         'quantity': item['quantity'],
                         'z_option': {'option_id': item['option_id'],
                                    'option_price': item['option_price'],
                                    'option_value': item['option_value'],
                                    'option_value_default': item['option_value_default']
                                    },
                         'shipping_code': item['shipping_code'],
                         'shipping_company_code': item['shipping_company_code'],
                         'shipping_company_id': item['shipping_company_id'],
                         'shipping_company_name': item['shipping_company_name'],
                         'status_code': item['status_code'],
                         'status_text': item['status_text'],
                         'tracking_no': item['tracking_no']
                         }
            item_list.append(item_json)
            product_no_list.append(item['product_no'])

        orders_json = {'order_id': order['order_id'],
                       'order_date': order['order_date'],
                       'order_items': item_list}
        orders_list.append(orders_json)

    # product 이미지 조회 및 데이터 가공
    product_str = ','.join(str(n) for n in set(product_no_list))
    request_url, headers = get_products_request_url(MallId, shop_no, AccessToken, product_str)
    response = requests.get(request_url, headers=headers)
    products = response.json()['products']

    for product in products:
        product_image_list[int(product['product_no'])] = {'detail_image': product['detail_image'],
                                                          'list_image': product['list_image'],
                                                          'small_image': product['small_image'],
                                                          'tiny_image': product['tiny_image']}

    # product image 삽입
    for order in orders_list:
        items = order['order_items']
        for item in items:
            item['z_product_image_url'] = product_image_list[int(item['product_no'])]

    return jsonify({'orders': orders_list})

# 회원의 3개월간 배송이 완료된 배송 상태를 조회하기 위한 API
@api.route('/delivered/')
def get_orders_delivered():
    src_name = request.args.get('src_name')
    member_id = request.args.get('member_id')
    page = int(request.args.get('page'))
    per_page = current_app.config['PER_PAGE']

    # accesstoken 확인 절차 및 주문조회
    mall_id, shop_no = get_mallid_shopno(src_name, 0)
    MallId, AccessToken = Confirm_access_expiration(mall_id, shop_no)
    request_url, headers = get_delivered_orders_request_url(MallId, shop_no, member_id, AccessToken, page, per_page)
    response = requests.get(request_url, headers=headers)
    orders = response.json()['orders']

    if len(orders) == 0:
        return jsonify({'orders': '배송상태에 있는 주문이 없습니다.'})

    if len(orders) < 3:
        next_url = None
    else:
        next_url = current_app.config['SERVER_URL'] + url_for('api.get_orders_delivered', mall_id=mall_id,
                                                              shop_no=shop_no, member_id=member_id, page=page + 1)
        orders.pop(-1)

    orders_list = list()
    product_no_list = list()
    product_image_list = dict()

    # data 가공처리중(product image 조회를 위한 작업도 동시에 진행)
    for order in orders:
        items = order['items']
        item_list = list()

        for item in items:
            item_json = {'order_item_code': item['order_item_code'],
                         'order_status': item['order_status'],
                         'product_code': item['product_code'],
                         'product_name': item['product_name'],
                         'product_no': item['product_no'],
                         'product_price': item['product_price'],
                         'quantity': item['quantity'],
                         'option': {'option_id': item['option_id'],
                                    'option_price': item['option_price'],
                                    'option_value': item['option_value'],
                                    'option_value_default': item['option_value_default']
                                    },
                         'shipping_code': item['shipping_code'],
                         'shipping_company_code': item['shipping_company_code'],
                         'shipping_company_id': item['shipping_company_id'],
                         'shipping_company_name': item['shipping_company_name'],
                         'status_code': item['status_code'],
                         'status_text': item['status_text'],
                         'tracking_no': item['tracking_no']
                         }
            item_list.append(item_json)
            product_no_list.append(item['product_no'])

        orders_json = {'order_id': order['order_id'],
                       'order_date': order['order_date'],
                       'order_items': item_list}
        orders_list.append(orders_json)

    # product 이미지 조회 및 데이터 가공
    product_str = ','.join(str(n) for n in set(product_no_list))
    request_url, headers = get_products_request_url(MallId, shop_no, AccessToken, product_str)
    response = requests.get(request_url, headers=headers)
    products = response.json()['products']

    for product in products:
        product_image_list[int(product['product_no'])] = {'detail_image': product['detail_image'],
                                                          'list_image': product['list_image'],
                                                          'small_image': product['small_image'],
                                                          'tiny_image': product['tiny_image']}

    # product image 삽입
    for order in orders_list:
        items = order['order_items']
        for item in items:
            item['product_image_url'] = product_image_list[int(item['product_no'])]

    return jsonify({'orders': orders_list, 'next_url': next_url, 'total_count': len(orders_list)})

#전화번호를 이용하여 회원의 아이디를 얻기 위한 API
@api.route('/user/')
def get_member_id():
    src_name = request.args.get('src_name')
    cellphone = request.args.get('cellphone')

    mall_id, shop_no = get_mallid_shopno(src_name, 0)
    MallId, AccessToken = Confirm_access_expiration(mall_id, shop_no)

    request_url, headers = get_member_id_request_url(MallId, shop_no, cellphone, AccessToken)

    response = requests.get(request_url, headers=headers)
    result = response.json()

    return jsonify(result)

# test하기 위한 API
@api.route('/test/')
def test():
    return 'test'