# 배송 조회를 위한 API

import requests
from . import api
from cafe24_app.api.AceessTokenHelper import *
from .UrlHelper import *
from flask import request, jsonify, current_app
from ..models import Scripttags


# 회원의 1개월간 모든 주문 상품을 조회하기위한 API
@api.route('/tracking/')
def get_orders():
    mall_id = request.args.get('mall_id')
    script_no = request.args.get('script_no')
    member_id = request.args.get('member_id')
    shop_no = Scripttags.query.filter_by(mall_id=mall_id).filter_by(script_no=script_no).first().shop_no

    MallId, AccessToken = Confirm_access_expiration(mall_id, shop_no)
    request_url, headers = get_order_request_url(MallId, member_id, AccessToken)

    order_status = {'입금전': 'N00', '상품 준비중': 'N10', '배송 준비중': 'N20', '배송 대기': 'N21', '배송 보류': 'N22', '배송 중': 'N30', '배송 완료': 'N40'}
    orders = {'입금전': None, '상품 준비중': None, '배송 준비중': None, '배송 대기': None, '배송 보류': None, '배송 중': None, '배송 완료': None}

    for key in order_status.keys():
        request_url_key = request_url + '&order_status=' + order_status[key]
        response = requests.get(request_url_key, headers=headers)
        result = response.json()
        orders[key] = result['orders']

    return jsonify(orders)

# 회원의 특정 상품의 배송 상태를 조회하기 위한 API
@api.route('/tracking/item/')
def specific_shipping_status():
    mall_id = request.args.get('mall_id')
    script_no = request.args.get('script_no')
    member_id = request.args.get('member_id')
    order_id = request.args.get('order_id')
    shop_no = Scripttags.query.filter_by(mall_id=mall_id).filter_by(script_no=script_no).first().shop_no

    MallId, AccessToken = Confirm_access_expiration(mall_id, shop_no)

    request_url, headers = specific_shipping_status_request_url(MallId, member_id, order_id, AccessToken)

    response = requests.get(request_url, headers=headers)
    result = response.json()

    return jsonify(result)

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

# test하기 위한 API
@api.route('/test/')
def test():
    mall_id = request.args.get('mall_id')
    script_no = request.args.get('script_no')
    shop_no = Scripttags.query.filter_by(mall_id=mall_id).filter_by(script_no=script_no).first().shop_no

    MallId, AccessToken = Confirm_access_expiration(mall_id, shop_no)

    request_url = 'https://' + MallId + '.' + current_app.config['REQUEST_BASE_PATH']+'/products'
    headers = {'Authorization': 'Bearer'+ ' ' + AccessToken, 'Content-Type': 'application/json'}

    response = requests.get(request_url, headers=headers)
    result = response.json()

    return jsonify(result)