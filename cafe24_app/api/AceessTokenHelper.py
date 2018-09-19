# 회원이 채팅을 사용할 때 AceessToken이 만료될경우 재발급을 위한 과정

from ..models import Mall
from datetime import datetime
from ..main.views import index


def Confirm_access_expiration(mall_id, shop_no):

    m = Mall.query.filter_by(mall_id=mall_id).filter_by(shop_no=shop_no).first()
    MallId = m.mall_id
    AccessToken = m.access_token
    expires_accesstoken = m.expires_at

    if expires_accesstoken < datetime.now():
        index()
        m = Mall.query.filter_by(mall_id=mall_id).filter_by(shop_no=shop_no).first()
        AccessToken = m.access_token
        MallId = m.mall_id

    return MallId, AccessToken
