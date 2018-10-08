from . import main
from .. import db
from ..models import Mall, Scripttags
from .UrlHelper import *
from fake_useragent import UserAgent
from flask import  redirect, url_for, request, session, current_app, jsonify
from datetime import datetime
import requests
import os

ua = UserAgent()

@main.route('/Uturn')
def Uturn():
    return '카페24용으로 개발되었습니다.'

@main.route('/callback')
def callback():
    code = request.args.get('code')
    mall_id = session['mall_id']
    credential = current_app.config['CLIENT_ID'] + ':' + current_app.config['CLIENT_SECRET']
    auth = b64encode(credential.encode()).decode()

    state = request.args.get('state')
    oauth_state = session['oauth_state']
    # print(state, oauth_state)  # 이걸 어떻게 활용하지?

    token_url, data, headers = callback_url(auth, code, mall_id)

    response = requests.post(token_url, headers=headers, data=data)
    result = response.json()

    mall = Mall.query.filter_by(mall_id=mall_id).first()
    mall.access_token = result.get('access_token')
    mall.refresh_token = result.get('refresh_token')
    mall.expires_at = datetime.strptime(result.get('expires_at'), '%Y-%m-%dT%H:%M:%S.%f')
    mall.refresh_token_expires_at = datetime.strptime(result.get('refresh_token_expires_at'), '%Y-%m-%dT%H:%M:%S.%f')

    db.session.add(mall)
    db.session.commit()

    create_src_url = "/creatscripttags/?mall_id=" + mall.mall_id + "&shop_no=" + str(mall.shop_no)
    return redirect(create_src_url)

@main.route('/')
def index():
    mall_id = request.args.get('mall_id')
    shop_no = request.args.get('shop_no')
    is_multi_shop = request.args.get('is_multi_shop')
    lang = request.args.get('lang')

    if mall_id is None and shop_no is None and is_multi_shop is None and lang is None:
        return redirect(url_for('main.Uturn'))

    session['mall_id'] = mall_id
    mall = Mall.query.filter_by(mall_id=mall_id).filter_by(shop_no=shop_no).first()

    if mall is None:
        m = Mall(mall_id=mall_id, shop_no=shop_no, is_multi_shop=is_multi_shop, lang=lang)
        db.session.add(m)
        db.session.commit()
        mall = m

    if mall.access_token is None:
        state, authorization_url = get_AccessToken_Url(mall_id)
        session['oauth_state'] = state
        return redirect(authorization_url)

    elif mall.refresh_token_expires_at < datetime.now():

        mall.access_token=None
        mall.refresh_token=None
        mall.expires_at=None
        mall.refresh_token_expires_at=None

        db.session.add(mall)
        db.session.commit()

        state, authorization_url = get_AccessToken_Url(mall_id)
        session['oauth_state'] = state
        return redirect(authorization_url)

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

        return 'hello'

    else:
        return 'hello'
@main.route('/accesstoken/')
def get_accesstoken:
    mall_id = request.args.get('mall_id')
    shop_no = request.args.get('shop_no')

    m = Mall.query.filter_by(mall_id=mall_id).filter_by(shop_no=shop_no).first()

    return jsonify({'accesstoken' : m.access_token })