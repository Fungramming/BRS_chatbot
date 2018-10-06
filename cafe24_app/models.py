from . import db, login
from flask_login import UserMixin
from sqlalchemy import Enum


class Mall(db.Model, UserMixin):
    __tablename__ = 'mall'
    id = db.Column(db.Integer, primary_key=True)
    mall_id = db.Column(db.String, nullable=False)
    shop_no = db.Column(db.Integer, default=1)
    is_multi_shop = db.Column(db.String, default=None)
    lang = db.Column(db.String, default='ko_KR')
    access_token = db.Column(db.String, default=None)
    refresh_token = db.Column(db.String, default=None)
    expires_at = db.Column(db.DateTime, default=None)
    refresh_token_expires_at = db.Column(db.DateTime, default=None)

    def __repr__(self):
        return '<Mall {}>'.format(self.mall_id)


@login.user_loader
def load_user(id):
    return Mall.query.get(int(id))

class Scripttags(db.Model):
    __tablename__ = 'scripttags'
    id = db.Column(db.Integer, primary_key=True)
    mall_id = db.Column(db.ForeignKey('mall.mall_id'), nullable=False)
    shop_no = db.Column(db.ForeignKey('mall.shop_no'), default=1)
    # mall_id = db.Column(db.String, nullable=False)
    # shop_no = db.Column(db.Integer, default=1)
    script_no = db.Column(db.Integer, unique=True)
    client_id = db.Column(db.String, nullable=False)
    src = db.Column(db.String, nullable=False)
    created_date = db.Column(db.DateTime, default=None)
    updated_date = db.Column(db.DateTime, default=None)
    JoinedLocationCode = db.Column(db.String, default='all')

    mall = db.relationship('Mall', primaryjoin='Scripttags.mall_id == Mall.mall_id', backref='mall_scripttags')
    mall1 = db.relationship('Mall', primaryjoin='Scripttags.shop_no == Mall.shop_no', backref='mall_scripttags_0')

    def __repr__(self):
        return '<Scripttags {}>'.format(self.script_no)


login.login_message = None

class FakeOrders(db.Model):
    __tablename__ = 'fakeorders'

    id = db.Column(db.Integer, primary_key=True)
    shop_no = db.Column(db.Integer, default=1)
    currency = db.Column(db.String, default='KRW')
    order_id = db.Column(db.String, unique=True)
    market_id = db.Column(db.String, default='self')
    buyer_name = db.Column(db.String, default=None)
    buyer_email = db.Column(db.String, default=None)
    buyer_phone = db.Column(db.String, default=None)
    buyer_cellphone = db.Column(db.String, default=None)
    member_id = db.Column(db.String, default=None)
    member_authentication = db.Column(db.Enum('T', 'B', 'J'), default='T')
    customer_group_no_when_ordering = db.Column(db.Integer, default=1)
    bank_code = db.Column(db.String, default='bank_26')
    bank_code_name = db.Column(db.String, default='Sample Bank')
    payment_method = db.Column(db.String, default='card')
    # payment_method_name = db.Column(db.String, default='Card')
    # payment_method_icon = db.Column(db.String, default="<img src='\/\/img.echosting.cafe24.com\/icon\/ico_pay_card.gif' alt='Card' title='Card'>")
    # payment_gateway_name = db.Column(db.String, default='')
    paid = db.Column(db.Enum('T', 'F'), default='T')
    order_date = db.Column(db.DateTime, default=None)
    # first_order = db.Column(db.String, default='F')
    payment_date = db.Column(db.DateTime, default=None)
    # order_from_mobile = db.Column(db.String, default='F')
    # order_price_amount = db.Column(db.String, default=None)
    # use_escrow = db.Column(db.String, default='F')
    # membership_discount_amount = db.Column(db.String, default='0.00')
    # actual_payment_amount = db.Column(db.String, default=None)
    # mileage_spent_amount = db.Column(db.String, default='0.00')
    # bank_account_no = db.Column(db.String, default='00000000000')
    # market_customer_id = db.Column(db.String, default=None)
    # payment_amount = db.Column(db.String, default=None)
    cancel_date = db.Column(db.DateTime, default=None)
    # inflow_name = db.Column(db.String, default='Web')
    # inflow_id = db.Column(db.String, default='self')
    # payment_confirmation = db.Column(db.String, default=None)
    # postpay_commission = db.Column(db.String, default='0.00')
    # postpay = db.Column(db.String, default='F')
    # shipping_fee = db.Column(db.String, default='0.00')
    # shipping_type = db.Column(db.String, default='A')
    # shipping_type_text = db.Column(db.String, default='Domestic Shipping')
    shipping_status = db.Column(db.Enum('F', 'M', 'T', 'W'), default='F')
    # wished_delivery_date = db.Column(db.String, default=None)
    # wished_delivery_time = db.Column(db.String, default=None)
    # wished_carrier_id = db.Column(db.String, default=None)
    # return_confirmed_date = db.Column(db.String, default=None)
    # total_supply_price = db.Column(db.String, default='3000')
    # additional_order_info_list = db.Column(db.String, default=None)
    # store_pickup = db.Column(db.String, default='F')
    # easypay_name = db.Column(db.String, default='')
    # loan_status = db.Column(db.String, default=None)
    # shipping_message = db.Column(db.String, default='')

    def __repr__(self):
        return '<FakeOrders {}>'.format(self.order_id)


class FakeOrderItems(db.Model):
    __tablename__ = 'fakeorderitem'
    id = db.Column(db.Integer, primary_key=True)
    shop_no = db.Column(db.Integer, default=1)
    item_no = db.Column(db.Integer, unique=True)
    order_item_code = db.Column(db.String, default=None)
    # variant_code = db.Column(db.String, default=None)
    product_no = db.Column(db.String, default=None)
    product_code = db.Column(db.String, default=None)
    eng_product_name = db.Column(db.String, default=None)
    # option_id = db.Column(db.String, default='000A')
    # option_value = db.Column(db.String, default='')
    # option_value_default = db.Column(db.String, default='')
    # additional_option_value = db.Column(db.String, default='')
    product_name = db.Column(db.String, default=None)
    # product_name_default = db.Column(db.String, default=None)
    product_price = db.Column(db.String, default=None)
    # option_price = db.Column(db.String, default='')
    # additional_discount_price = db.Column(db.String, default='')
    quantity = db.Column(db.String, default='1')
    # supplier_product_name = db.Column(db.String, default='')
    supplier_transaction_type = db.Column(db.Enum('D', 'P'), default='D')
    # supplier_id = db.Column(db.String, default='S0000000')
    # supplier_name = db.Column(db.String, default='king')
    tracking_no = db.Column(db.String, default='00000000')
    shipping_code = db.Column(db.String)
    # post_express_flag = db.Column(db.String, default=None)
    order_status = db.Column(db.Enum('N00', 'N10', 'N20', 'N21', 'N22', 'N30', 'N40'))
    # order_status_additional_info = db.Column(db.String, default=None)
    status_code = db.Column(db.Enum('N1', 'N2', 'C1', 'C2', 'C3', 'E1'), default='N1')
    status_text = db.Column(db.Enum('정상', '교환상품', '입금전 취소', '배송전취소', '반품', '교환'), default='정상')
    # open_market_status = db.Column(db.String, default='')
    # bundled_shipping_type = db.Column(db.String, default='N')
    shipping_company_id = db.Column(db.String, default='2')
    shipping_company_name = db.Column(db.String, default='DHL')
    shipping_company_code = db.Column(db.String, default='0001')
    # product_bundle = db.Column(db.Eunm('T', 'F'), default='F')
    # product_bundle_no = db.Column(db.String, default='0')
    # product_bundle_name = db.Column(db.String, default=None)
    # product_bundle_name_default = db.Column(db.String, default=None)
    # product_bundle_type = db.Column(db.String, default='c')
    # was_product_bundle = db.Column(db.String, default=None)
    # original_bundle_item_no = db.Column(db.String, default=None)
    # naver_pay_order_id = db.Column(db.String, default=None)
    # naver_pay_claim_status = db.Column(db.String, default='PAYMENT_WAITING')
    # individual_shipping_fee = db.Column(db.String, default='0.00')
    # shipping_fee_type = db.Column(db.String, default='X')
    # shipping_fee_type_text = db.Column(db.String, default='Free')
    # payment_info_id = db.Column(db.String, default='0')
    original_item_no = db.Column(db.String, default='')
    # store_pickup = db.Column(db.String, default='F')
    ordered_date = db.Column(db.DateTime, default=None)
    shipped_date = db.Column(db.DateTime, default=None)
    delivered_date = db.Column(db.DateTime, default=None)
    cancel_date = db.Column(db.DateTime, default=None)
    return_request_date = db.Column(db.DateTime, default=None)
    return_date = db.Column(db.DateTime, default=None)
    cancel_request_date = db.Column(db.DateTime, default=None)
    refund_date = db.Column(db.DateTime, default=None)
    exchange_request_date = db.Column(db.DateTime, default=None)
    exchange_date = db.Column(db.DateTime, default=None)
    # product_material = db.Column(db.String, default=None)
    # product_material_eng = db.Column(db.String, default=None)
    # cloth_fabric = db.Column(db.String, default=None)
    # product_weight = db.Column(db.String, default=None)
    # volume_size = db.Column(db.String, default=None)
    # volume_size_weight = db.Column(db.String, default=None)
    # clearance_category_code = db.Column(db.String, default=None)
    # clearance_category_code_info = db.Column(db.String, default=None)
    # clearance_category_code_base = db.Column(db.String, default=None)
    # hs_code = db.Column(db.String, default='')
    # one_plus_n_event = db.Column(db.String, default=None)
    # origin_place = db.Column(db.String, default='')
    # gift = db.Column(db.String, default='F')

    def __repr__(self):
        return '<fakeorderitem {}>'.format(self.order_item_code)


class FakeProduct(db.Model):
    __tablename__ = 'fakeproduct'
    id = db.Column(db.Integer, primary_key=True)
    shop_no = db.Column(db.Integer, default=1)
    product_no = db.Column(db.Integer)
    product_code = db.Column(db.String)
    custom_product_code = db.Column(db.String, default='')
    product_name = db.Column(db.String)
    # eng_product_name = db.Column(db.String, default='')
    # supply_product_name = db.Column(db.String, default='')
    # model_name = db.Column(db.String, default='')
    price = db.Column(db.String)
    # retail_price = db.Column(db.String, default='0.00')
    supply_price = db.Column(db.String)
    display = db.Column(db.String, default='F')
    # selling = db.Column(db.String, default='F')
    # product_condition = db.Column(db.String, default='N')
    # summary_description = db.Column(db.String, default='')
    # margin_rate = db.Column(db.String, default='10.00')
    # tax_type = db.Column(db.String, default='A')
    # tax_amount = db.Column(db.Integer, default='10')
    # price_content = db.Column(db.String, default=None)
    # buy_limit_type = db.Column(db.String, default='F')
    # buy_unit_type = db.Column(db.String, default='P')
    # buy_unit = db.Column(db.Integer, default=1)
    # order_quantity_limit_type = db.Column(db.String, default='O')
    # minimum_quantity = db.Column(db.Integer, default=1)
    # maximum_quantity = db.Column(db.Integer, default=10)
    # mileage_amount = db.Column(db.String, default=None)
    # except_member_mileage = db.Column(db.String, default='F')
    # adult_certification = db.Column(db.String, default='F')
    detail_image = db.Column(db.String, default=None)
    list_image = db.Column(db.String, default=None)
    tiny_image = db.Column(db.String, default=None)
    small_image = db.Column(db.String, default=None)
    # has_option = db.Column(db.String, default='F')
    # option_type = db.Column(db.String, default=None)
    # manufacturer_code = db.Column(db.String, default='M0000000')
    # trend_code = db.Column(db.String, default='T0000000')
    # brand_code = db.Column(db.String, default='B0000000')
    # supplier_code = db.Column(db.String, default='S0000000')
    # made_date = db.Column(db.String, default='')
    # release_date = db.Column(db.String, default='')
    # expiration_strat_date = db.Column(db.String, default='')
    # expiration_end_date = db.Column(db.String, default='')
    # origin_classification = db.Column(db.String, default='F')
    # origin_place_no = db.Column(db.Integer, default='1798')
    # origin_place_value = db.Column(db.String, default='')
    # icon_show_start = db.Column(db.String, default=None)
    # icon_show_end = db.Column(db.String, default=None)
    # icon_num = db.Column(db.Integer, default=0)
    # hscode = db.Column(db.String, default=None)
    # product_weight = db.Column(db.Integer, default='1.00')
    # product_material = db.Column(db.String, default='')
    created_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime)
    # english_product_material = db.Column(db.String, default='')
    # cloth_fabric = db.Column(db.String, default=None)
    # soldout_icon = db.Column(db.Boolean, default=False)
    # recommend_icon = db.Column(db.Boolean, default=False)
    # new_icon = db.Column(db.Boolean, default=False)
    # approve_status = db.Column(db.String, default='')
    # classification_code = db.Column(db.String, default='C000000A')
    # sold_out = db.Column(db.String, default='F')
    # additional_price = db.Column(db.String, default=None)

    def __repr__(self):
        return '<FakeOrders {}>'.format(self.product_no)







class FakeCustomer(db.Model):
    __tablename__ = 'fakecustomer'
    id = db.Column(db.Integer, primary_key=True)
    shop_no = db.Column(db.Integer, default=1)
    member_id = db.Column(db.String)
    name = db.Column(db.String)
    available_mileage = db.Column(db.String, default='00.00')
    group_no = db.Column(db.Integer, default=1)
    member_authentication = db.Column(db.String, default='T')
    use_blacklist = db.Column(db.String, default='F')
    blacklist_type = db.Column(db.String, default='')
    phone_number = db.Column(db.String, default=None)

    def __repr__(self):
        return '<FakeOrders {}>'.format(self.member_id)