from . import main
from .. import db
from ..models import Mall, Script
from fake_useragent import UserAgent
from flask import render_template, redirect, url_for, jsonify, request, session, g
from flask_login import login_required, login_user, current_user, logout_user
from requests_oauthlib.oauth2_session import OAuth2Session

from datetime import datetime
import requests, json, base64

ua = UserAgent()

@main.route('/')
def index():
    return '카페24용으로 개발되었습니다.'