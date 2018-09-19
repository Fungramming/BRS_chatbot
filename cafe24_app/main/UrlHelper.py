# view파일을 위한 URL 관

from flask import current_app
from ..helper import random_str
from urllib.parse import urlencode
from base64 import b64encode

# AccessToken을 얻기위한 URL
def get_AccessToken_Url(mall_id):

    authorization_base_url = 'https://' + mall_id + '.' + current_app.config['AUTHORIZATION_BASE_PATH']

    client_id = current_app.config['CLIENT_ID']
    scope = current_app.config['SCOPE']
    redirect_url = current_app.config['REDIRECT_URL']
    state = random_str(30, 1)

    query = {'response_type': 'code', 'client_id': client_id, 'scope': scope,
             'redirect_uri': redirect_url, 'state': state}

    authorization_url = authorization_base_url + '?' + urlencode(query)

    return state, authorization_url

# AccessToken의 재발급을 위한 URL
def reissue_AcessToken_Url(refresh_token, mall_id):
    credential = current_app.config['CLIENT_ID'] + ':' + current_app.config['CLIENT_SECRET']
    auth = b64encode(credential.encode()).decode()

    headers = {'Authorization': 'Basic' + ' ' + auth, 'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'grant_type': 'refresh_token', 'refresh_token': refresh_token}

    token_url = 'https://' + mall_id + '.' + current_app.config['TOKEN_BASE_PATH']

    return token_url, data, headers

# callback URL
def callback_url(auth, code, mall_id):
    headers = {'Authorization': 'Basic' + ' ' + auth, 'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'grant_type': 'authorization_code', 'code': code, 'redirect_uri': current_app.config['REDIRECT_URL']}

    token_url = 'https://' + mall_id + '.' + current_app.config['TOKEN_BASE_PATH']

    return token_url, data, headers