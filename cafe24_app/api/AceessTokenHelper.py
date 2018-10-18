# 회원이 채팅을 사용할 때 AceessToken이 만료될경우 재발급을 위한 과정
import requests
from cafe24_app.models import Mall
from datetime import datetime
from flask import jsonify
from ..main.UrlHelper import reissue_AcessToken_Url, get_AccessToken_Url
from .. import db


def Confirm_access_expiration(mall_id, shop_no):
    mall = Mall.query.filter_by(mall_id=mall_id).filter_by(shop_no=shop_no).first()

    if mall.refresh_token_expires_at < datetime.now():
        return None, None

    elif mall.expires_at < datetime.now():

        m = Mall.query.filter_by(mall_id=mall_id).filter_by(shop_no=shop_no).first()
        token_url, data, headers = reissue_AcessToken_Url(m.refresh_token, mall_id)
        response = requests.post(token_url, data=data, headers=headers)
        result = response.json()

        mall.access_token = result.get('access_token')
        mall.refresh_token = result.get('refresh_token')
        mall.expires_at = datetime.strptime(result.get('expires_at'), '%Y-%m-%dT%H:%M:%S.%f')
        mall.refresh_token_expires_at = datetime.strptime(result.get('refresh_token_expires_at'),
                                                          '%Y-%m-%dT%H:%M:%S.%f')

        db.session.add(mall)
        db.session.commit()

        return mall.mall_id, mall.access_token
    else:
        return mall.mall_id, mall.access_token



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
