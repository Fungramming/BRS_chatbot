from flask import current_app
from base64 import b64encode
from . import db
from .models import Mall
from datetime import datetime
import random as r
import requests


def random_str(length, blocks):
    random_string = ''
    random_str_seq = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i in range(0, length*blocks):
        if i % length == 0 and i != 0:
            random_string += '-'
        random_string += str(random_str_seq[r.randint(0, len(random_str_seq) - 1)])
    return random_string


def fetch_access_token(mall_id):
    mall = Mall.query.filter_by(mall_id=mall_id).first()

    credential = current_app.config['CLIENT_ID'] + ':' + current_app.config['CLIENT_SECRET']
    auth = b64encode(credential.encode()).decode()
    refresh_token = mall.refresh_token

    headers = {'Authorization': 'Basic' + ' ' + auth, 'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'grant_type': 'refresh_token', 'refresh_token': refresh_token}

    token_url = 'https://' + mall_id + '.' + current_app.config['TOKEN_BASE_PATH']

    response = requests.post(token_url, data=data, headers=headers)
    result = response.json()

    mall.access_token = result.get('access_token')
    mall.refresh_token = result.get('refresh_token')
    mall.expires_at = datetime.strptime(result.get('expires_at'), '%Y-%m-%dT%H:%M:%S.%f')
    mall.refresh_token_expires_at = datetime.strptime(result.get('refresh_token_expires_at'),
                                                      '%Y-%m-%dT%H:%M:%S.%f')

    db.session.add(mall)
    db.session.commit()