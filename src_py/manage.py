#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-11-20
# @Author  : zhoujie

import os
import re
import json

from datetime import datetime
from xlrd import xldate_as_tuple
from flask import Flask, g, jsonify, make_response, request
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from passlib.apps import custom_app_context
import flask_excel as excel
from werkzeug import SharedDataMiddleware
from werkzeug.utils import secure_filename

# basedir = os.path.abspath(os.path.dirname(__file__))

# app = Flask(__name__)
from __init__ import app, db
import SQLManage
import excel2db
Admin        = SQLManage.Admin
JoinInfos    = SQLManage.JoinInfos
HistoryData  = excel2db.HistoryData
listAirClogA = excel2db.listAirClogA
listAirClogB = excel2db.listAirClogB
listSizeNH3Actual = excel2db.listSizeNH3Actual
listSizeNH3Demand = excel2db.listSizeNH3Demand
listAirDeposiA = excel2db.listAirDeposiA
listAirDeposiB = excel2db.listAirDeposiB

# r'/*' 是通配符，让本服务器所有的 URL 都允许跨域请求
CORS(app, resources=r'/*')
CORS(app, supports_credentials=True)

auth = HTTPBasicAuth()
CSRF_ENABLED = True
app.debug = True

@app.route('/api/getdrawAirClogChart', methods=['GET'])
@auth.login_required
def getdrawAirClogChart():
    return jsonify({'code':200, 
                   'listAirClogA':listAirClogA,
                   'listAirClogB':listAirClogB,
                   })

@app.route('/api/getdrawSizeNH3Chart', methods=['GET'])
@auth.login_required
def getdrawSizeNH3Chart():
    return jsonify({'code':200, 
                   'listSizeNH3Actual':listSizeNH3Actual,
                   'listSizeNH3Demand':listSizeNH3Demand,
                   })

@app.route('/api/getdrawAirDeposiChart', methods=['GET'])
@auth.login_required
def getdrawAirDeposiChart():
    return jsonify({'code':200, 
                   'listAirDeposiA':listAirDeposiA,
                   'listAirDeposiB':listAirDeposiB
                   })

# 密码校验
@auth.verify_password
def verify_password(name_or_token, password):
    if not name_or_token:
        return False
    name_or_token = re.sub(r'^"|"$', '', name_or_token)
    admin = Admin.verify_auth_token(name_or_token)
    if not admin:
        admin = Admin.query.first()
        # admin = Admin.query.filter_by(name=name_or_token).first()
        if not admin or not admin.verify_password(password):
            return False
    g.admin = admin
    return True


@app.route('/api/login', methods=['POST'])
@auth.login_required
def get_auth_token():
    token = g.admin.generate_auth_token()
    return jsonify({'code': 200, 'msg': "登录成功", 'token': token.decode('ascii'), 'name': g.admin.name})

#test
@app.route('/get', methods=['GET', 'POST'])
def get():
    name = request.args.get('name', '')
    if name == 'xuefeilong':
        age = 21
    else:
        age = 'valid name'
    return jsonify(
        data={name: age},
        extra={
            'total': '120'
        }
    )


@app.route('/api/setpwd', methods=['POST'])
@auth.login_required
def set_auth_pwd():
    data = json.loads(str(request.data, encoding="utf-8"))
    admin = Admin.query.filter_by(name=g.admin.name).first()
    if admin and admin.verify_password(data['oldpass']) and data['confirpass'] == data['newpass']:
        admin.hash_password(data['newpass'])
        return jsonify({'code': 200, 'msg': "密码修改成功"})
    else:
        return jsonify({'code': 500, 'msg': "请检查输入"})


@app.route('/api/users/listpage', methods=['GET'])
@auth.login_required
def get_user_list():
    page_size = 8
    page = request.args.get('page', 1, type=int)
    name = request.args.get('name', '')
    query = db.session.query
    if name:
        Infos = query(JoinInfos).filter(JoinInfos.name.like('%{}%'.format(name)))
        print('name Infos',Infos)
    else:
        Infos = query(JoinInfos)
        print('Infos',Infos)
    total = Infos.count()
    print('total',total)
    if not page:
        Infos = Infos.all()
    else:
        Infos = Infos.offset((page - 1) * page_size).limit(page_size).all()
    return jsonify({
        'code': 200,
        'total': total,
        'page_size': page_size,
        'infos': [u.to_dict() for u in Infos]
    })


@app.route('/api/user/remove', methods=['GET'])
@auth.login_required
def remove_user():
    remove_id = request.args.get('id', type=int)
    if remove_id:
        remove_info = JoinInfos.query.get_or_404(remove_id)
        db.session.delete(remove_info)
        return jsonify({'code': 200, 'msg': "删除成功"})
    else:
        return jsonify({'code': 500, 'msg': "未知错误"})


@app.route('/api/user/bathremove', methods=['GET'])
@auth.login_required
def bathremove_user():
    remove_ids = request.args.get('ids')
    is_current = False
    if remove_ids:
        for remove_id in remove_ids:
            remove_info = JoinInfos.query.get(remove_id)
            if remove_info:
                is_current = True
                db.session.delete(remove_info)
            else:
                pass
        print(remove_ids, remove_info)
        if is_current:
            return jsonify({'code': 200, 'msg': "删除成功"})
        else:
            return jsonify({'code': 404, 'msg': "请正确选择"})
    else:
        return jsonify({'code': 500, 'msg': "未知错误"})

# excel数据交互
@app.route('/api/upload', methods=['GET', 'POST'])
# @auth.login_required
def upload():
    if request.method == 'POST':
        f = request.files['file']
    basepath = os.path.dirname(__file__)
    upload_path = os.path.join(basepath, '../static/excel', secure_filename(f.filename))
    f.save(upload_path)
    print("upload test ok")
    # return "ok"
    # return render_template('upload_ok.html')
    # print(request.files)
    # file = request.files['file']
    # print('file', type(file), file)
    print(f.filename)    # 打印文件名
 
    # f = file.read()    #文件内容upload
    # data = xlrd.open_workbook(file_contents=f)
    # table = data.sheets()[0]
    # names = data.sheet_names()  # 返回book中所有工作表的名字
    # status = data.sheet_loaded(names[0])  # 检查sheet1是否导入完毕
    # print(status)
    # nrows = table.nrows  # 获取该sheet中的有效行数
    # ncols = table.ncols  # 获取该sheet中的有效列数
    # print(nrows)
    # print(ncols)
    # s = table.col_values(0)  # 第1列数据
    # for i in s:
    #     ii = i.strip()
    #     print(len(ii))
    return 'OK'


@app.route('/api/getdrawStackedAreaChart', methods=['GET'])
@auth.login_required
def getdrawStackedAreaChart():
    return jsonify({'code':200, 'x':20, 'y':50})

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


if __name__ == '__main__':
    db.create_all()
    app.run(host='127.0.0.1',port=5000)