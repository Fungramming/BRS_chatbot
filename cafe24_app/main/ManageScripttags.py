import requests
from . import main
from ..api.AceessTokenHelper import *
from .UrlHelper import post_scripttags_url, get_specific_scripttags_url, delete_scripttags_url, get_scripttags_url, update_scripttags_url
from ..models import Scripttags
from flask import request, jsonify, current_app, redirect
from cafe24_app import db
from datetime import datetime

# script tag 생성하는 API
@main.route('/creatscripttags/')
def Create_Scripttags():
    mall_id = request.args.get('mall_id')
    shop_no = request.args.get('shop_no')
    src = current_app.config['SRC_URL']

    MallId, AccessToken = Confirm_access_expiration(mall_id, shop_no)

    request_url, headers, json = post_scripttags_url(MallId, AccessToken, shop_no, src)

    response = requests.post(request_url, headers=headers, json=json)
    result = response.json()

    scripttag = Scripttags.query.filter_by(mall_id=mall_id).filter_by(shop_no=shop_no).first()

    if scripttag is None:
        scripttag = result['scripttag']
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
        result = {'to users': 'Hello', 'respons_messeage': 'Create Success', 'scripttag': scripttag}
    else:
        mall = Mall.query.filter_by(mall_id=mall_id).filter_by(shop_no=shop_no).first()
        update_src_url = "/updatescripttags/?mall_id=" + mall.mall_id + "&shop_no=" + str(mall.shop_no)\
                         + "&src=" + str(scripttag.script_no)
        return redirect(update_src_url)

    return jsonify(result)

# script tag
@main.route('/updatescripttags/')
def Update_Scripttags():
    mall_id = request.args.get('mall_id')
    shop_no = request.args.get('shop_no')
    script_no = request.args.get('script_no')
    src = current_app.config['SRC_URL']

    MallId, AccessToken = Confirm_access_expiration(mall_id, shop_no)

    if script_no == None:
        scripttag = Scripttags.query.filter_by(mall_id=mall_id).filter_by(shop_no=shop_no).first()
        script_no = scripttag.script_no

    request_url, headers, json = update_scripttags_url(MallId, AccessToken, script_no, shop_no, src)

    response = requests.put(request_url, headers=headers, json=json)
    result = response.json()
    scripttag = result['scripttag']

    st = Scripttags.query.filter_by(mall_id=mall_id).filter_by(shop_no=shop_no).first()

    st.script_no = scripttag['script_no']
    st.src = scripttag['src']
    st.updated_date = datetime.strptime(scripttag['updated_date'].split('+')[0], '%Y-%m-%dT%H:%M:%S')

    db.session.add(st)
    db.session.commit()

    return jsonify({'respons_messeage': 'Update Success', 'scripttag': scripttag})


@main.route('/deletescripttags/')
def Delete_Scripttags():
    mall_id = request.args.get('mall_id')
    shop_no = request.args.get('shop_no')

    MallId, AccessToken = Confirm_access_expiration(mall_id, shop_no)

    scripttag = Scripttags.query.filter_by(mall_id=mall_id).filter_by(shop_no=shop_no).first()

    if scripttag is None:
        # result = {'respons_messeage': 'Delete Error', 'error_message': 'Script tag가 존재하지 않습니다.'}
        script_no = '1538446067058703'

        request_url, headers = delete_scripttags_url(MallId, AccessToken, script_no)

        response = requests.delete(request_url, headers=headers)
        r = response.json()

        st = Scripttags.query.filter_by(mall_id=mall_id).filter_by(shop_no=shop_no).first()

        db.session.delete(st)
        db.session.commit()
        result = {'respons_messeage': 'Delete Success', 'scripttag': r['scripttag']}

    else:
        script_no = scripttag.script_no

        request_url, headers = delete_scripttags_url(MallId, AccessToken, script_no)

        response = requests.delete(request_url, headers=headers)
        r = response.json()

        st = Scripttags.query.filter_by(mall_id=mall_id).filter_by(shop_no=shop_no).first()

        db.session.delete(st)
        db.session.commit()
        result = {'respons_messeage': 'Delete Success', 'scripttag': r['scripttag']}

    return jsonify(result)


@main.route('/getscripttags/')
def Get_Scripttags():
    mall_id = request.args.get('mall_id')
    shop_no = request.args.get('shop_no')

    MallId, AccessToken = Confirm_access_expiration(mall_id, shop_no)

    scripttag = Scripttags.query.filter_by(mall_id=mall_id).filter_by(shop_no=shop_no).first()
    if scripttag == None:
        result = {'error': 'scripttag가 존재하지 않습니다.'}
    else:
        script_no = scripttag.script_no

        request_url, headers = get_specific_scripttags_url(MallId, AccessToken, script_no)

        response = requests.get(request_url, headers=headers)
        r = response.json()
        result = {'respons_messeage': 'Script tag for our app', 'scripttag': r['scripttag']}

    return jsonify(result)


@main.route('/getscripttagsall/')
def Get_Scripttags_all():
    mall_id = request.args.get('mall_id')
    shop_no = request.args.get('shop_no')

    MallId, AccessToken = Confirm_access_expiration(mall_id, shop_no)

    request_url, headers = get_scripttags_url(MallId, AccessToken)

    response = requests.get(request_url, headers=headers)
    result = response.json()

    return jsonify({'respons_messeage': 'All sript tags used by mall', 'scripttags': result['scripttags']})
