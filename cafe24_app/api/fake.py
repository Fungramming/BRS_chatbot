from random import randint, choice
from datetime import datetime, timedelta
from . import api
from cafe24_app import db
import requests
from flask import request, jsonify
from cafe24_app.api.AceessTokenHelper import Confirm_access_expiration
from cafe24_app.api.UrlHelper import get_member_id_request_url, get_products_request_url
from cafe24_app.models import FakeCustomer, FakeProduct, FakeOrders, FakeOrderItems


@api.route('/createfakedata/')
def create_Fake_Data():
    # 이전의 가짜데이터 청소하기(충돌방지)
    db.session.query(FakeCustomer).delete()
    db.session.commit()
    db.session.query(FakeProduct).delete()
    db.session.commit()
    db.session.query(FakeOrders).delete()
    db.session.commit()
    db.session.query(FakeOrderItems).delete()
    db.session.commit()

    # 변수선언
    mall_id = 'blackrubydev'
    shop_no = '1'
    on = int(request.args.get('order_num'))
    phonelist = list()
    faketime = (datetime.today() - timedelta(days=3)).strftime('%Y%m%d')
    order_dates = list()

    # 쇼핑몰 유저 데이터 local DB로 저장
    for i in range(0, 5):
        i = str(i + 1)
        PN = '010-' + i + i + i + i + '-' + i + i + i + i
        phonelist.append(PN)

    MallId, AccessToken = Confirm_access_expiration(mall_id, shop_no)

    for pn in phonelist:
        cellphone = pn
        request_url, headers = get_member_id_request_url(MallId, cellphone, AccessToken)
        response = requests.get(request_url, headers=headers)
        result = response.json()
        r_cover=result.get('customers')
        r=r_cover[0]
        fc = FakeCustomer(shop_no = r['member_id'],
                         member_id = r['member_id'],
                         name  = r['name'],
                         available_mileage  = r['available_mileage'],
                         group_no  = r['group_no'],
                         member_authentication  = r['member_authentication'],
                         use_blacklist  = r['use_blacklist'],
                         blacklist_type  = r['blacklist_type'],
                          phone_number = cellphone)

        db.session.add(fc)
    db.session.commit()

    # 쇼핑몰 상품 데이터 local DB로 저장
    request_url, headers = get_products_request_url(MallId, AccessToken)

    response = requests.get(request_url, headers=headers)
    result = response.json()
    r_cover = result.get('products')
    for r in r_cover:
        fp = FakeProduct(shop_no=r['shop_no'],
                         product_no=r['product_no'],
                         product_code=r['product_code'],
                         product_name=r['product_name'],
                         price=r['price'],
                         supply_price=r['supply_price'],
                         detail_image=r['detail_image'],
                         list_image=r['list_image'],
                         tiny_image=r['tiny_image'],
                         small_image=r['small_image'],
                         created_date=datetime.strptime(r['created_date'].split('+')[0], '%Y-%m-%dT%H:%M:%S'),
                         updated_date=datetime.strptime(r['updated_date'].split('+')[0], '%Y-%m-%dT%H:%M:%S'),
                         )
        db.session.add(fp)
    db.session.commit()

    for num in range(0,on):
        i = round(num / 10) + 3
        faketime1 = (datetime.today() - timedelta(days=i)).strftime('%Y%m%d')
        order_dates.append(datetime.strptime(faketime1, '%Y%m%d') + timedelta(hours=randint(1, 24),
                                                                        minutes=randint(0, 60),
                                                                        seconds=randint(0, 60)))
    order_dates.sort()
    for od in order_dates:
        faketime1 = od.strftime('%Y%m%d')
        if faketime == faketime1:
            count += 1
            id_num = str(count).zfill(7)
            order_id = faketime1 + '-' + id_num
        else:
            count = 1
            faketime = faketime1
            id_num = str(count).zfill(7)
            order_id = faketime1 + '-' + id_num

        # 구매자 가져오기
        phone_number = choice(phonelist)
        customer = FakeCustomer.query.filter_by(phone_number=phone_number).first()

        # 구매 여부 및 상태 생성
        order_status = choice(['N00', 'N10', 'N20', 'N21', 'N22', 'N30', 'N40'])

        fo= FakeOrders(shop_no = shop_no,
                       order_id = order_id,
                       buyer_name = customer.name,
                       buyer_cellphone = customer.phone_number,
                       member_id = customer.member_id,
                       member_authentication= customer.member_authentication,
                       customer_group_no_when_ordering = customer.group_no,
                       order_status = order_status
        )

        range_item = randint(2,4)
        for i in range(1,range_item):
            id_list = [1, 2, 3, 4]
            id = choice(id_list)
            product = FakeProduct.query.filter_by(id=id).first()
            foi = FakeOrderItems(shop_no = shop_no,
                                 item_no =i,
                                 order_item_code = order_id + '-'+ str(i).zfill(2),
                                 product_no = product.product_no,
                                 product_code = product.product_code,
                                 product_name = product.product_name,
                                 product_price = product.price,
                                 quantity = randint(1,3),
                                 tracking_no = status['tracking_no'],
                                 shipping_code = status['shipping_code'],
                                 order_status = order_status,
                                 status_code = status['status_code'],
                                 ordered_date = status['order_date'],
                                 shipped_date = status['shipped_date'],
                                 delivered_date = status['delivered_date'],
                                 cancel_date = status['cancel_date'],
                                 return_request_date = status['return_request_date'],
                                 return_date = status['return_date'],
                                 cancel_request_date = status['cancel_request_date'],
                                 refund_date = status['refund_date'],
                                 exchange_request_date = status['exchange_request_date'],
                                 exchange_date = status['exchange_date']
                                 )



    return jsonify({'result': 'create success'})

@api.route('/cleanfakedata/')
def Clean_Fake_Data():

    db.session.query(FakeCustomer).delete()
    db.session.commit()
    db.session.query(FakeProduct).delete()
    db.session.commit()
    db.session.query(FakeOrders).delete()
    db.session.commit()

    return jsonify({'result': 'clean success'})

@api.route('/producttest/')
def Insert_product_data():
    id_list=[1,2,3,4]
    id = choice(id_list)
    product = FakeProduct.query.filter_by(id=id).first()
    print(product.product_name)
    print(type(product))
    return jsonify({'test': 'success'})

