import requests
import random
from . import main
from ..api.AceessTokenHelper import *
from .UrlHelper import post_scripttags_url, get_specific_scripttags_url, delete_scripttags_url, get_scripttags_url, update_scripttags_url
from ..models import Scripttags
from flask import request, jsonify, current_app, redirect
from cafe24_app import db
from datetime import datetime

# Script tag 생성하는 API (양쪽 DB를 모두 리셋 후 생성하는 방식으로 작동)
@main.route('/creatscripttags/')
def Create_Scripttags():
    mall_id = request.args.get('mall_id')
    shop_no = request.args.get('shop_no')
    display_code = request.args.get('display_code')
    src = current_app.config['SRC_BASE_URL'] + current_app.config['SRC_DEFUALT_FILE']

    MallId, AccessToken = Confirm_access_expiration(mall_id, shop_no)

    # remote script tag 초기화 과정
    request_url, headers = get_scripttags_url(MallId, AccessToken)
    response = requests.get(request_url, headers=headers)
    scripttags = response.json()['scripttags']

    for sc in scripttags:
        if sc['client_id'] == current_app.config['CLIENT_ID']:
            request_url, headers = delete_scripttags_url(MallId, AccessToken, sc['script_no'])
            response = requests.delete(request_url, headers=headers)
        else:
            pass


    # local script tage 초기화 과정
    st = Scripttags.query.filter_by(mall_id=mall_id).filter_by(shop_no=shop_no).all()

    if st is not None:
        for ss in st:
            db.session.delete(ss)
            db.session.commit()
    else:
        pass

    # script tag 생성
    request_url, headers, json = post_scripttags_url(MallId, AccessToken, shop_no, src)
    response = requests.post(request_url, headers=headers, json=json)
    result = response.json()

    scripttag = result['scripttag']
    src = current_app.config['SRC_BASE_URL'] + mall_id + '_' + scripttag['script_no'] + '.js'
    st = Scripttags(mall_id=mall_id,
                    shop_no=scripttag['shop_no'],
                    script_no=scripttag['script_no'],
                    client_id=scripttag['client_id'],
                    src=src,
                    created_date=datetime.strptime(scripttag['created_date'].split('+')[0], '%Y-%m-%dT%H:%M:%S'),
                    updated_date=datetime.strptime(scripttag['updated_date'].split('+')[0], '%Y-%m-%dT%H:%M:%S'),
                    )
    db.session.add(st)
    db.session.commit()

    request_url, headers, json = update_scripttags_url(MallId, AccessToken, scripttag['script_no'], shop_no, src, display_code)
    response = requests.put(request_url, headers=headers, json=json)
    result = response.json()

    result = {'to users': 'Hello', 'respons_messeage': 'Create Success', 'scripttag': result['scripttag']}

    return jsonify(result)

# Script tag를 수정하는 API(Cafe24 서버에서 에러로 응답이 올시 생성 API로 리다이렉트 한다.)
@main.route('/updatescripttags/')
def Update_Scripttags():
    mall_id = request.args.get('mall_id')
    shop_no = request.args.get('shop_no')
    display_code = request.args.get('display_code')
    script_no = None

    MallId, AccessToken = Confirm_access_expiration(mall_id, shop_no)

    scripttag = Scripttags.query.filter_by(mall_id=mall_id).filter_by(shop_no=shop_no).first()

    if scripttag == None:
        mall = Mall.query.filter_by(mall_id=mall_id).filter_by(shop_no=shop_no).first()
        create_src_url = "/creatscripttags/?mall_id=" + mall.mall_id + "&shop_no=" + str(mall.shop_no) +'&display_code=' + display_code
        return redirect(create_src_url)
    else:
        script_no = scripttag.script_no
        src = scripttag.src

    request_url, headers, json = update_scripttags_url(MallId, AccessToken, script_no, shop_no, src, display_code)

    response = requests.put(request_url, headers=headers, json=json)
    result = response.json()

    if 'error' in result:
        mall = Mall.query.filter_by(mall_id=mall_id).filter_by(shop_no=shop_no).first()
        create_src_url = "/creatscripttags/?mall_id=" + mall.mall_id + "&shop_no=" + str(mall.shop_no) +'&display_code=' + display_code
        return redirect(create_src_url)

    scripttag = result['scripttag']

    st = Scripttags.query.filter_by(mall_id=mall_id).filter_by(shop_no=shop_no).first()

    st.script_no = scripttag['script_no']
    st.src = scripttag['src']
    st.updated_date = datetime.strptime(scripttag['updated_date'].split('+')[0], '%Y-%m-%dT%H:%M:%S')
    st.JoinedLocationCode = display_code or 'all'

    db.session.add(st)
    db.session.commit()

    return jsonify({'respons_messeage': 'Update Success', 'scripttag': scripttag})

# Script tag 삭제하는 API (에러시 새로 무조건 삭제하는 방식으로 작동)
@main.route('/deletescripttags/')
def Delete_Scripttags():
    mall_id = request.args.get('mall_id')
    shop_no = request.args.get('shop_no')
    script_no = None

    MallId, AccessToken = Confirm_access_expiration(mall_id, shop_no)

    scripttag = Scripttags.query.filter_by(mall_id=mall_id).filter_by(shop_no=shop_no).first()

    if scripttag is not None:
        script_no = scripttag.script_no
        db.session.delete(scripttag)
        db.session.commit()

        request_url, headers = delete_scripttags_url(MallId, AccessToken, script_no)
        response = requests.delete(request_url, headers=headers)
        r = response.json()

        if 'error' in r:
            if r['error']['code'] == 404:
                result = {'respons_messeage': 'Delete only local DB', 'status': r['error']}
            else:
                result = {'respons_messeage': '....모르겠다...젠장'}
        else:
            result = {'respons_messeage': 'Delete Success', 'status': r['scripttag']}

    else:
        request_url, headers = get_scripttags_url(MallId, AccessToken)
        response = requests.get(request_url, headers=headers)
        r = response.json()

        for st in r['scripttags']:
            if st['client_id'] == current_app.config['CLIENT_ID']:
                script_no = st['script_no']

        if script_no == None:
            result = {'respons_messeage': 'No need to delete', 'status': 'Ok'}
        else:
            request_url, headers = delete_scripttags_url(MallId, AccessToken, script_no)
            response = requests.delete(request_url, headers=headers)
            r = response.json()
            result = {'respons_messeage': 'Delete Success', 'status': r['scripttag']}

    return jsonify(result)


# Script tag 조회하는 API (조회시 에러가 나면 Cafe24 서버의 상태로 적용한다.)
@main.route('/getscripttags/')
def Get_Scripttags():
    mall_id = request.args.get('mall_id')
    shop_no = request.args.get('shop_no')
    script_no = None

    MallId, AccessToken = Confirm_access_expiration(mall_id, shop_no)

    scripttag = Scripttags.query.filter_by(mall_id=mall_id).filter_by(shop_no=shop_no).first()

    if scripttag == None:
        request_url, headers = get_scripttags_url(MallId, AccessToken)
        response = requests.get(request_url, headers=headers)
        r = response.json()

        for st in r['scripttags']:
            if st['client_id'] == current_app.config['CLIENT_ID']:
                script_no = st['script_no']

        if script_no == None:
            result = {'error': 'Script does not exist in local and remote'}
        else:
            request_url, headers = get_specific_scripttags_url(MallId, AccessToken, script_no)
            response = requests.get(request_url, headers=headers)
            r = response.json()

            scripttag = r['scripttag']
            st = Scripttags(mall_id=mall_id,
                            shop_no=scripttag['shop_no'],
                            script_no=scripttag['script_no'],
                            client_id=scripttag['client_id'],
                            src=scripttag['src'],
                            created_date=datetime.strptime(scripttag['created_date'].split('+')[0], '%Y-%m-%dT%H:%M:%S'),
                            updated_date=datetime.strptime(scripttag['updated_date'].split('+')[0], '%Y-%m-%dT%H:%M:%S')
                            )
            db.session.add(st)
            db.session.commit()

            result = {'respons_messeage': 'Script tag for our app', 'scripttag': r['scripttag']}

    else:
        script_no = scripttag.script_no
        request_url, headers = get_specific_scripttags_url(MallId, AccessToken, script_no)
        response = requests.get(request_url, headers=headers)
        r = response.json()

        if 'error' in r:
            result = {'respons_messeage': 'Script does not exist in remote.', 'status': r['error']}
            db.session.delete(scripttag)
            db.session.commit()
        else:
            result = {'respons_messeage': 'Script tag for our app', 'scripttag': r['scripttag']}

    return jsonify(result)

# 모든 Script tag를 조회하는 API
@main.route('/getscripttagsall/')
def Get_Scripttags_all():
    mall_id = request.args.get('mall_id')
    shop_no = request.args.get('shop_no')

    MallId, AccessToken = Confirm_access_expiration(mall_id, shop_no)

    request_url, headers = get_scripttags_url(MallId, AccessToken)

    response = requests.get(request_url, headers=headers)
    result = response.json()

    return jsonify({'respons_messeage': 'All sript tags used by mall', 'scripttags': result['scripttags']})
