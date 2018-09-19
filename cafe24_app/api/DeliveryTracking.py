import requests
from . import api
from .AceessTokenHelper import *
from .UrlHelper import *
from ..models import Mall
from flask import request, jsonify, current_app


# 회원의 1개월간 모든 주문 상품을 조회하기위한 API
@api.route('/tracking/')
def get_orders():
    mall_id = request.args.get('mall_id')
    shop_no = request.args.get('shop_no')
    member_id = request.args.get('member_id')

    MallId, AccessToken = Confirm_access_expiration(mall_id, shop_no)

    request_url, headers = get_order_request_url(MallId, member_id, AccessToken)

    response = requests.get(request_url, headers=headers)
    result = response.json()

    orders = result['orders']
    delivery_complete = list()
    delivery_Notcomplete = list()

    for order in orders:
        shipping_status=order['shipping_status']
        if shipping_status == 'T':
            delivery_complete.append(order)
        else:
            delivery_Notcomplete.append(order)


    return jsonify({
        'delivery_complete': delivery_complete,
        'delivery_Notcomplete': delivery_Notcomplete
    })

# 회원의 특정 상품의 배송 상태를 조회하기 위한 API
@api.route('/tracking/item/')
def specific_shipping_status():
    mall_id = request.args.get('mall_id')
    shop_no = request.args.get('shop_no')
    member_id = request.args.get('member_id')
    order_id = request.args.get('order_id')

    MallId, AccessToken = Confirm_access_expiration(mall_id, shop_no)

    request_url, headers = specific_shipping_status_request_url(MallId, member_id, order_id, AccessToken)

    response = requests.get(request_url, headers=headers)
    result = response.json()

    return jsonify(result)

#전화번호를 이용하여 회원의 아이디를 얻기 위한 API
@api.route('/user/')
def get_member_id():
    mall_id = request.args.get('mall_id')
    shop_no = request.args.get('shop_no')
    cellphone = request.args.get('cellphone')

    MallId, AccessToken = Confirm_access_expiration(mall_id, shop_no)

    request_url, headers = get_member_id_request_url(MallId, cellphone, AccessToken)

    response = requests.get(request_url, headers=headers)
    result = response.json()

    return jsonify(result)

# test하기 위한 API
@api.route('/test/')
def test():

    mall_id = request.args.get('mall_id')
    shop_no = request.args.get('shop_no')

    m = Mall.query.filter_by(mall_id=mall_id).filter_by(shop_no=shop_no).first()

    request_url = 'https://' + m.mall_id + '.' + current_app.config['REQUEST_BASE_PATH']+'/products'
    headers = {'Authorization': 'Bearer'+ ' ' + m.access_token, 'Content-Type': 'application/json'}

    response = requests.get(request_url, headers=headers)
    result = response.json()

    products=result['products']
    products_delivery_complete = list()
    products_delivery_Notcomplete = list()

    for p in products:
        a=p['product_condition']
        if a == 'R':
            products_delivery_complete.append(p)
        else:
            products_delivery_Notcomplete.append(p)

    return jsonify({
        'products_delivery_complete' : products_delivery_complete,
        'products_delivery_Notcomplete' : products_delivery_Notcomplete
    })