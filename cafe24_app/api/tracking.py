import requests
from . import api
from .date import orders_date_range
from ..models import Mall
from flask import request, jsonify, current_app

# 회원의 1개월간 모든 주문 상품을 조회한다.
@api.route('/tracking/')
def get_orders():
    start ,end = orders_date_range()

    mall_id = request.args.get('mall_id')
    shop_no = request.args.get('shop_no')
    member_id = request.args.get('member_id')

    m = Mall.query.filter_by(mall_id=mall_id).filter_by(shop_no=shop_no).first()

    request_url = 'https://' + m.mall_id + '.' + current_app.config['REQUEST_BASE_PATH']+\
                  '/orders?start_date='+start+'&end_date='+end+'&member_id='+member_id+'&date_type=order_date'
    headers = {'Authorization': 'Bearer'+ ' ' + m.access_token, 'Content-Type': 'application/json'}

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

@api.route('/user/')
def get_member_id():
    mall_id = request.args.get('mall_id')
    shop_no = request.args.get('shop_no')
    cellphone = request.args.get('cellphone')
    m = Mall.query.filter_by(mall_id=mall_id).filter_by(shop_no=shop_no).first()
    request_url = 'https://' + m.mall_id + '.' + current_app.config['REQUEST_BASE_PATH'] + '/customers?cellphone=' + cellphone
    headers = {'Authorization': 'Bearer'+ ' ' + m.access_token, 'Content-Type': 'application/json'}

    response = requests.get(request_url, headers=headers)
    result = response.json()

    return jsonify(result)


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