from . import cafe24
from .. import db
from ..models import Mall, Script
from fake_useragent import UserAgent
from flask import render_template, redirect, url_for, jsonify, request, session, current_app, g
from flask_login import login_required, login_user, current_user, logout_user
from requests_oauthlib.oauth2_session import OAuth2Session

from datetime import datetime
import requests, json, base64

ua = UserAgent()

@cafe24.route('/')
def index():
    mall_id = request.args.get('mall_id') or 'blackrubydev'
    session['mall_id'] = mall_id
    authorization_base_url = 'https://' + mall_id + '.' + current_app.config['AUTHORIZATION_BASE_PATH']

    client_id = current_app.config['CLIENT_ID']
    scope = current_app.config['SCOPE']

    cafe_24 = OAuth2Session(client_id, redirect_uri='https://127.0.0.1:5000/cafe24/callback', scope=scope)
    authorization_url, state = cafe_24.authorization_url(authorization_base_url)

    session['oauth_state'] = state
    return redirect(authorization_url)

@cafe24.route('/callback')
def callback():
    code = request.args.get('code')
    mall_id = session['mall_id']
    state = session['oauth_state']

    print(code, mall_id, state)

    return 'hello'