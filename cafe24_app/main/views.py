from . import main
from .. import db
from ..models import Mall
from ..helper import random_str
from fake_useragent import UserAgent
from flask import render_template, redirect, url_for, jsonify, request, session, g,  current_app
from flask_login import login_required, login_user, current_user, logout_user
from requests_oauthlib.oauth2_session import OAuth2Session

from datetime import datetime
from urllib.parse import urlencode
from base64 import b64encode
import requests

ua = UserAgent()

@main.route('/Uturn')
def Uturn():
    return '카페24용으로 개발되었습니다.'

@main.route('/callback')
def callback():
    code = request.args.get('code')
    state = request.args.get('state')
    mall_id = session['mall_id']
    oauth_state = session['oauth_state']
    credential = current_app.config['CLIENT_ID'] + ':' + current_app.config['CLIENT_SECRET']
    auth = b64encode(credential.encode()).decode()
    print(state, oauth_state)

    headers = {'Authorization': 'Basic' + ' ' + auth, 'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'grant_type': 'authorization_code', 'code': code, 'redirect_uri': current_app.config['REDIRECT_URL']}

    # cafe_24 = OAuth2Session(current_app.config['CLIENT_ID'], state=state,
    #                        redirect_uri=current_app.config['REDIRECT_URL'],
    #                        scope=current_app.config['SCOPE'])
    # custom_headers = {'User-Agent': ua.random}

    token_url = 'https://' + mall_id + '.' + current_app.config['TOKEN_BASE_PATH']

    # token = cafe_24.fetch_token(token_url, client_id=current_app.config['CLIENT_ID'],
    #                             client_secret=current_app.config['CLIENT_SECRET'], authorization_response=request.url,
    #                             headers=custom_headers)

    response = requests.post(token_url, data=data, headers=headers)
    result = response.json()

    mall = Mall.query.filter_by(mall_id=mall_id).first()
    mall.access_token = result.get('access_token')
    mall.refresh_token = result.get('refresh_token')
    mall.expires_at = datetime.strptime(result.get('expires_at'), '%Y-%m-%dT%H:%M:%S.%f')
    mall.refresh_token_expires_at = datetime.strptime(result.get('refresh_token_expires_at'), '%Y-%m-%dT%H:%M:%S.%f')

    db.session.add(mall)
    db.session.commit()

    return 'hello'

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

        authorization_base_url = 'https://' + mall_id + '.' + current_app.config['AUTHORIZATION_BASE_PATH']

        client_id = current_app.config['CLIENT_ID']
        scope = current_app.config['SCOPE']
        redirect_url = current_app.config['REDIRECT_URL']
        state = random_str(30, 1)

        query = {'response_type': 'code', 'client_id': client_id, 'scope': scope,
                 'redirect_uri': redirect_url, 'state': state}

        authorization_url = authorization_base_url + '?' + urlencode(query)

        # cafe_24 = OAuth2Session(client_id, redirect_uri='https://127.0.0.1:5000/callback', scope=scope)
        # authorization_url, state = cafe_24.authorization_url(authorization_base_url)
        print(state)

        session['oauth_state'] = state
        return redirect(authorization_url)

    elif mall.expires_at < datetime.now():
        pass
        #리프레쉬 토큰으로 재발급

    elif mall.refresh_token_expires_at < datetime.now():
        pass
        #띠용

    else:
        return 'hello'