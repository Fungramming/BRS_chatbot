import requests
from . import main
from ..api.AceessTokenHelper import *
from .UrlHelper import post_scripttags_url, get_specific_scripttags_url, delete_scripttags_url, get_scripttags_url, update_scripttags_url
from ..models import Scripttags, Mall
from flask import request, current_app, redirect
from cafe24_app import db
from datetime import datetime
from flask_responses import json_response

# Script tag 생성하는 API (양쪽 DB를 모두 리셋 후 생성하는 방식으로 작동)
@main.route('/creatscripttags/', methods=['POST','PUT'])
def Create_Scripttags():
    mall_id = request.args.get('mall_id')
    shop_no = request.args.get('shop_no')
    display_code = request.args.get('display_code')
    color = request.args.get('color')
    height = request.args.get('height')
    transparency = request.args.get('transparency')
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
    m = Mall.query.filter_by(mall_id=mall_id).filter_by(shop_no=shop_no).first()
    st = Scripttags.query.filter_by(mall_idx=m.idx).all()

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
    src_name = mall_id + '_' + scripttag['script_no']
    src_url = current_app.config['SRC_BASE_URL'] + src_name + '.js'

    st = Scripttags(mall_idx=m.idx,
                    script_no=scripttag['script_no'],
                    client_id=scripttag['client_id'],
                    src_url=src_url,
                    created_date=datetime.strptime(scripttag['created_date'].split('+')[0], '%Y-%m-%dT%H:%M:%S'),
                    updated_date=datetime.strptime(scripttag['updated_date'].split('+')[0], '%Y-%m-%dT%H:%M:%S'),
                    JoinedLocationCode=display_code,
                    color=color,
                    height=height,
                    transparency=transparency,
                    )

    db.session.add(st)
    db.session.commit()

    # Mall table에 src_name 삽입
    m = Mall.query.filter_by(mall_id=mall_id).filter_by(shop_no=shop_no).first()
    m.src_name = src_name

    db.session.add(m)
    db.session.commit()

    request_url, headers, json = update_scripttags_url(MallId, AccessToken, scripttag['script_no'], shop_no, src_url, display_code)
    response = requests.put(request_url, headers=headers, json=json)
    result = response.json()

    st = Scripttags.query.filter_by(script_no=result['scripttag']['script_no']).first()

    result = {'to users': 'Hello', 'respons_messeage': 'Create Success', 'scripttag': st.to_json()}

    return json_response(result, status_code=response.status_code)

# Script tag를 수정하는 API(Cafe24 서버에서 에러로 응답이 올시 생성 API로 리다이렉트 한다.)
@main.route('/updatescripttags/', methods=['PUT'])
def Update_Scripttags():
    mall_id = request.args.get('mall_id')
    shop_no = request.args.get('shop_no')
    display_code = request.args.get('display_code')
    color = request.args.get('color')
    height = request.args.get('height')
    transparency = request.args.get('transparency')
    script_no = None

    MallId, AccessToken = Confirm_access_expiration(mall_id, shop_no)

    m = Mall.query.filter_by(mall_id=mall_id).filter_by(shop_no=shop_no).first()
    st = Scripttags.query.filter_by(mall_idx=m.idx).first()

    if st == None:
        create_src_url = current_app.config['SERVER_URL'] + "/creatscripttags/?mall_id=" + m.mall_id + "&shop_no=" + str(m.shop_no) +\
                         '&display_code=' + display_code + '&color=' + color + '&height=' + height + '&transparency=' + transparency
        return redirect(create_src_url, code=307)

    else:
        script_no = st.script_no
        src_url = st.src_url

    request_url, headers, json = update_scripttags_url(MallId, AccessToken, script_no, shop_no, src_url, display_code)

    response = requests.put(request_url, headers=headers, json=json)
    result = response.json()

    if 'error' in result:
        create_src_url = current_app.config['SERVER_URL'] + "/creatscripttags/?mall_id=" + m.mall_id + "&shop_no=" + str(m.shop_no) +'&display_code=' + display_code
        return redirect(create_src_url, code=307)

    scripttag = result['scripttag']

    st.script_no = scripttag['script_no']
    st.src_url = scripttag['src']
    st.updated_date = datetime.strptime(scripttag['updated_date'].split('+')[0], '%Y-%m-%dT%H:%M:%S')
    st.JoinedLocationCode = display_code
    st.color = color
    st.height = height
    st.transparency = float(transparency)

    db.session.add(st)
    db.session.commit()

    st = Scripttags.query.filter_by(mall_idx=m.idx).first()

    return json_response({'respons_messeage': 'Update Success', 'scripttag': st.to_json()}, status_code=response.status_code)

# Script tag 삭제하는 API (에러시 새로 무조건 삭제하는 방식으로 작동)
@main.route('/deletescripttags/', methods=['DELETE'])
def Delete_Scripttags():
    mall_id = request.args.get('mall_id')
    shop_no = request.args.get('shop_no')
    script_no = None

    MallId, AccessToken = Confirm_access_expiration(mall_id, shop_no)

    m = Mall.query.filter_by(mall_id=mall_id).filter_by(shop_no=shop_no).first()
    scripttag = Scripttags.query.filter_by(mall_idx=m.idx).first()

    if scripttag is not None:
        script_no = scripttag.script_no
        db.session.delete(scripttag)
        db.session.commit()

        request_url, headers = delete_scripttags_url(MallId, AccessToken, script_no)
        response = requests.delete(request_url, headers=headers)
        r = response.json()

        if 'error' in r:
            return json_response(r, status_code=response.status_code)
        else:
            result = {'respons_messeage': 'Delete Success', 'status': r['scripttag']}
            return json_response(result, status_code=response.status_code)

    else:
        request_url, headers = get_scripttags_url(MallId, AccessToken)
        response = requests.get(request_url, headers=headers)
        r = response.json()

        for st in r['scripttags']:
            if st['client_id'] == current_app.config['CLIENT_ID']:
                script_no = st['script_no']

        if script_no == None:
            result = {'respons_messeage': 'No need to delete', 'status': 'Ok'}
            return json_response(result, status_code=202)
        else:
            request_url, headers = delete_scripttags_url(MallId, AccessToken, script_no)
            response = requests.delete(request_url, headers=headers)
            r = response.json()
            result = {'respons_messeage': 'Delete Success', 'status': r['scripttag']}
            return json_response(result, status_code=response.status_code)




# Script tag 조회하는 API (조회시 에러가 나면 Cafe24 서버의 상태로 적용한다.)
@main.route('/getscripttags/', methods=['GET'])
def Get_Scripttags():
    mall_id = request.args.get('mall_id')
    shop_no = request.args.get('shop_no')
    script_no = None

    MallId, AccessToken = Confirm_access_expiration(mall_id, shop_no)

    m = Mall.query.filter_by(mall_id=mall_id).filter_by(shop_no=shop_no).first()
    scripttag = Scripttags.query.filter_by(mall_idx=m.idx).first()

    if scripttag == None:
        request_url, headers = get_scripttags_url(MallId, AccessToken)
        response = requests.get(request_url, headers=headers)
        r = response.json()

        for st in r['scripttags']:
            if st['client_id'] == current_app.config['CLIENT_ID']:
                script_no = st['script_no']

        if script_no == None:
            result = {'error': 'Script does not exist in local and remote'}
            return json_response(result, status_code=404)
        else:
            request_url, headers = get_specific_scripttags_url(MallId, AccessToken, script_no)
            response = requests.get(request_url, headers=headers)
            r = response.json()

            st = Scripttags(mall_idx=m.idx,
                            script_no=r['scripttag']['script_no'],
                            client_id=r['scripttag']['client_id'],
                            src=scripttag['src'],
                            created_date=datetime.strptime(r['scripttag']['created_date'].split('+')[0], '%Y-%m-%dT%H:%M:%S'),
                            updated_date=datetime.strptime(r['scripttag']['updated_date'].split('+')[0], '%Y-%m-%dT%H:%M:%S'),
                            JoinedLocationCode=",".join(r['scripttag']['display_location']))
            db.session.add(st)
            db.session.commit()

            s = Scripttags.query.filter_by(script_no=r['scripttag']['script_no']).first()

            result = {'respons_messeage': 'Script tag for our app', 'scripttag': s.to_json()}
            return json_response(result, status_code=response.status_code)

    else:
        script_no = scripttag.script_no
        request_url, headers = get_specific_scripttags_url(MallId, AccessToken, script_no)
        response = requests.get(request_url, headers=headers)
        r = response.json()

        if 'error' in r:
            result = {'respons_messeage': 'Script does not exist in remote.', 'status': r['error']}
            db.session.delete(scripttag)
            db.session.commit()
            return json_response(result, status_code=response.status_code)
        else:
            s = Scripttags.query.filter_by(script_no=r['scripttag']['script_no']).first()

            result = {'respons_messeage': 'Script tag for our app', 'scripttag': s.to_json()}
            return json_response(result, status_code=response.status_code)

# 모든 Script tag를 조회하는 API
@main.route('/getscripttagsall/', methods=['GET'])
def Get_Scripttags_all():
    mall_id = request.args.get('mall_id')
    shop_no = request.args.get('shop_no')

    MallId, AccessToken = Confirm_access_expiration(mall_id, shop_no)

    request_url, headers = get_scripttags_url(MallId, AccessToken)

    response = requests.get(request_url, headers=headers)
    result = response.json()

    return json_response({'respons_messeage': 'All sript tags used by mall', 'scripttags': result['scripttags']}, status_code=response.status_code)

@main.route('/getscriptoption/', methods=['GET'])
def Get_Script_option():
    src_name = request.args.get('src_name')

    mall_id, shop_no, mall_idx = get_mallid_shopno(src_name, 1)
    if mall_id is None or shop_no is None or mall_idx is None:
        return json_response({'error': 'mall does not exist'}, status_code=404)

    MallId, AccessToken = Confirm_access_expiration(mall_id, shop_no)
    sc = Scripttags.query.filter_by(mall_idx=mall_idx).first()

    if sc is None:
        return json_response({'error': 'Script does not exist'}, status_code=404)
    option = {'JoinedLocationCode': sc.JoinedLocationCode,
              'color': sc.color,
              'height': sc.height,
              'transparency': sc.transparency
              }

    return json_response({'option': option}, status_code=200)