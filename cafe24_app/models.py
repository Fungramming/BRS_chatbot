from . import db, login
from flask_login import UserMixin


class Mall(db.Model, UserMixin):
    __tablename__ = 'mall'
    idx = db.Column(db.Integer, primary_key=True)
    mall_id = db.Column(db.String(45), nullable=False)
    shop_no = db.Column(db.Integer, default=1)
    is_multi_shop = db.Column(db.String(4), default=None)
    lang = db.Column(db.String(4), default='ko_KR')
    access_token = db.Column(db.String(200), default=None)
    refresh_token = db.Column(db.String(200), default=None)
    expires_at = db.Column(db.DateTime, default=None)
    refresh_token_expires_at = db.Column(db.DateTime, default=None)
    src_name = db.Column(db.String(45), default=None)

    def __repr__(self):
        return '<Mall {}>'.format(self.mall_id)

    def to_json(self):
        json = {
            'idx': self.idx,
            'mall_id': self.mall_id,
            'shop_no': self.shop_no,
            'is_multi_shop': self.is_multi_shop,
            'lang': self.lang,
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'expires_at': self.expires_at,
            'refresh_token_expires_at': self.refresh_token_expires_at,
            'src_name': self.src_name
        }
        return json


@login.user_loader
def load_user(idx):
    return Mall.query.get(int(idx))

class Scripttags(db.Model):
    __tablename__ = 'scripttags'
    idx = db.Column(db.Integer, primary_key=True)
    mall_idx = db.Column(db.ForeignKey('mall.idx'), nullable=False)
    script_no = db.Column(db.String(45), unique=True)
    client_id = db.Column(db.String(45), nullable=False)
    src_url = db.Column(db.String(200), nullable=False)
    created_date = db.Column(db.DateTime, default=None)
    updated_date = db.Column(db.DateTime, default=None)
    JoinedLocationCode = db.Column(db.Text, default='all')
    color = db.Column(db.String(45), default='rgb(10,91,255)')
    height = db.Column(db.Integer, default=80)
    transparency = db.Column(db.Float, default=1.0)

    mall = db.relationship('Mall', primaryjoin='Scripttags.mall_idx == Mall.idx', backref='mall_scripttags')

    def __repr__(self):
        return '<Scripttags {}>'.format(self.script_no)

    def to_json(self):
        json = {
            'idx': self.idx,
            'mall_idx': self.mall_idx,
            'script_no': self.script_no,
            'client_id': self.client_id,
            'src': self.src,
            'created_date': self.created_date,
            'updated_date': self.updated_date,
            'JoinedLocationCode': self.JoinedLocationCode,
            'color': self.color,
            'height': self.height,
            'transparency': self.transparency
        }
        return json


login.login_message = None

# class FakeOrders(db.Model):
#     __tablename__ = 'fakeorders'
#
#     id = db.Column(db.Integer, primary_key=True)
#     shop_no = db.Column(db.Integer, default=1)
#     currency = db.Column(db.String, default='KRW')
#     order_id = db.Column(db.String, unique=True)
#     market_id = db.Column(db.String, default='self')
#     buyer_name = db.Column(db.String, default=None)
#     buyer_email = db.Column(db.String, default=None)
#     buyer_phone = db.Column(db.String, default=None)
#     buyer_cellphone = db.Column(db.String, default=None)
#     member_id = db.Column(db.String, default=None)
#     member_authentication = db.Column(db.Enum('T', 'B', 'J'), default='T')
#     customer_group_no_when_ordering = db.Column(db.Integer, default=1)
#     order_status = db.Column(db.Enum('N00', 'N10', 'N20', 'N21', 'N22', 'N30', '40'))
#
#     def __repr__(self):
#         return '<FakeOrders {}>'.format(self.order_id)
#
#
# class FakeOrderItems(db.Model):
#     __tablename__ = 'fakeorderitem'
#     id = db.Column(db.Integer, primary_key=True)
#     shop_no = db.Column(db.Integer, default=1)
#     item_no = db.Column(db.Integer, unique=True)
#     order_item_code = db.Column(db.String, default=None)
#     product_no = db.Column(db.String, default=None)
#     product_code = db.Column(db.String, default=None)
#     eng_product_name = db.Column(db.String, default=None)
#     product_name = db.Column(db.String, default=None)
#     product_price = db.Column(db.String, default=None)
#     quantity = db.Column(db.String, default='1')
#     supplier_transaction_type = db.Column(db.Enum('D', 'P'), default='D')
#     tracking_no = db.Column(db.String, default='00000000')
#     shipping_code = db.Column(db.String)
#     order_status = db.Column(db.Enum('N00', 'N10', 'N20', 'N21', 'N22', 'N30', 'N40'))
#     status_code = db.Column(db.Enum('N1', 'N2', 'C1', 'C2', 'C3', 'E1'), default='N1')
#     status_text = db.Column(db.Enum('정상', '교환상품', '입금전 취소', '배송전취소', '반품', '교환'), default='정상')
#     shipping_company_id = db.Column(db.String, default='2')
#     shipping_company_name = db.Column(db.String, default='DHL')
#     shipping_company_code = db.Column(db.String, default='0001')
#     original_item_no = db.Column(db.String, default='')
#     ordered_date = db.Column(db.DateTime, default=None)
#     shipped_date = db.Column(db.DateTime, default=None)
#     delivered_date = db.Column(db.DateTime, default=None)
#     cancel_date = db.Column(db.DateTime, default=None)
#     return_request_date = db.Column(db.DateTime, default=None)
#     return_date = db.Column(db.DateTime, default=None)
#     cancel_request_date = db.Column(db.DateTime, default=None)
#     refund_date = db.Column(db.DateTime, default=None)
#     exchange_request_date = db.Column(db.DateTime, default=None)
#     exchange_date = db.Column(db.DateTime, default=None)
#
#     def __repr__(self):
#         return '<fakeorderitem {}>'.format(self.order_item_code)
#
#
# class FakeProduct(db.Model):
#     __tablename__ = 'fakeproduct'
#     id = db.Column(db.Integer, primary_key=True)
#     shop_no = db.Column(db.Integer, default=1)
#     product_no = db.Column(db.Integer)
#     product_code = db.Column(db.String)
#     custom_product_code = db.Column(db.String, default='')
#     product_name = db.Column(db.String)
#     price = db.Column(db.String)
#     supply_price = db.Column(db.String)
#     display = db.Column(db.String, default='F')
#     detail_image = db.Column(db.String, default=None)
#     list_image = db.Column(db.String, default=None)
#     tiny_image = db.Column(db.String, default=None)
#     small_image = db.Column(db.String, default=None)
#     created_date = db.Column(db.DateTime)
#     updated_date = db.Column(db.DateTime)
#
#     def __repr__(self):
#         return '<FakeOrders {}>'.format(self.product_no)
#
#
#
#
#
#
#
# class FakeCustomer(db.Model):
#     __tablename__ = 'fakecustomer'
#     id = db.Column(db.Integer, primary_key=True)
#     shop_no = db.Column(db.Integer, default=1)
#     member_id = db.Column(db.String)
#     name = db.Column(db.String)
#     available_mileage = db.Column(db.String, default='00.00')
#     group_no = db.Column(db.Integer, default=1)
#     member_authentication = db.Column(db.String, default='T')
#     use_blacklist = db.Column(db.String, default='F')
#     blacklist_type = db.Column(db.String, default='')
#     phone_number = db.Column(db.String, default=None)
#
#     def __repr__(self):
#         return '<FakeOrders {}>'.format(self.member_id)