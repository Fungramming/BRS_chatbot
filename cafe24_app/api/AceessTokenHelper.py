# 회원이 채팅을 사용할 때 AceessToken이 만료될경우 재발급을 위한 과정
import requests
from cafe24_app.models import Mall
from datetime import datetime
from flask import current_app
from cafe24_app.main.views import index


def Confirm_access_expiration(mall_id, shop_no):

    m = Mall.query.filter_by(mall_id=mall_id).filter_by(shop_no=shop_no).first()
    MallId = m.mall_id
    ShopNo = str(m.shop_no)
    IsMultiShop = m.is_multi_shop
    AccessToken = m.access_token
    Lang = m.lang
    expires_accesstoken = m.expires_at

    if expires_accesstoken < datetime.now():
        request_url = current_app.config['SERVER_URL'] + '/?mall_id='+MallId+'&shop_no='+ShopNo+'&is_multi_shop='+IsMultiShop+'&lang='+Lang
        response = requests.get(request_url)

        MallId, AccessToken = get_access_token(MallId, ShopNo)
        return MallId, AccessToken
    else:
        return MallId, AccessToken


def get_mallid_shopno(src_name, mode):
    # mode에따라 출력값이 다름/ '1': mall_idx 추가로 return 한다.
    m = Mall.query.filter_by(src_name=src_name).first()
    mall_id = m.mall_id
    shop_no = str(m.shop_no)

    if mode == 1:
        mall_idx = m.idx
        return mall_id, shop_no, mall_idx
    else:
        return mall_id, shop_no

def get_access_token(MallId, ShopNo):
    m = Mall.query.filter_by(mall_id=MallId).filter_by(shop_no=ShopNo).first()
    AccessToken = m.access_token
    MallId = m.mall_id

    return MallId, AccessToken