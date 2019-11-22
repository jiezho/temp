#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-11-20
# @Author  : zhoujie

import os
import re
import json
from datetime import datetime

from flask import Flask, g, jsonify, make_response, request
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from passlib.apps import custom_app_context

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# r'/*' 是通配符，让本服务器所有的 URL 都允许跨域请求
CORS(app, resources=r'/*')
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
# 配置不变: 后期可以放在配置文件中
HOSTNAME = 'localhost'
PORT = '3306'
DATABASE = 'rdkx'
USERNAME = 'root'
PASSWORD = '000000'
DB_URI = "mysql+pymysql://{}:{}@{}:{}/{}".format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
 
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
db = SQLAlchemy(app)

auth = HTTPBasicAuth()
CSRF_ENABLED = True
app.debug = True

# 创建导入的数据数据库模型
class JoinInfos(db.Model):
    __tablename__ = 'joininfos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), index=True)
    groupA = db.Column(db.Integer)
    groupB = db.Column(db.Integer)
    unit = db.Column(db.String(64))

    def __repr__(self):
        return "<JoinInfos:%s>"%self.name

    def to_dict(self):
        columns = self.__table__.columns.keys()
        result = {}
        for key in columns:
            if key == 'pub_date':
                value = getattr(self, key).strftime("%Y-%m-%d %H:%M:%S")
            else:
                value = getattr(self, key)
            result[key] = value
        return result

# ‘登录用户’数据库模型
class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True)
    password = db.Column(db.String(128))

    # 密码加密
    def hash_password(self, password):
        self.password = custom_app_context.encrypt(password)

    # 密码解析
    def verify_password(self, password):
        return custom_app_context.verify(password, self.password)

    # 获取token，有效时间100min
    def generate_auth_token(self, expiration=6000):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    # 解析token，确认登录的用户身份
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        admin = Admin.query.get(data['id'])
        return admin
 

# 将模型映射到数据库中
db.drop_all()
db.create_all()

# 添加数据
rdkx_user = Admin(id="8",name="rdkx",password="$5$rounds=535000$9WoOVzcj7Fvi3FsJ$EnhMCR6iPrgkp3G1iulbz5dAw9apErh2UrbyVD6JQP7")
db.session.add(rdkx_user)
db.session.commit()

infos1 = JoinInfos(id='1', name='机组负荷', groupA='22', groupB='15.6', unit='MW')
infos2 = JoinInfos(id='2', name='烟气侧压差', groupA='233', groupB='15.6', unit='kPa')
infos3 = JoinInfos(id='3', name='堵塞系数', groupA='22', groupB='15.6', unit='')
infos4 = JoinInfos(id='4', name='堵塞速度', groupA='22', groupB='15.6', unit='%/天')
infos5 = JoinInfos(id='5', name='脱硝实际喷氨量', groupA='-90', groupB='15.6', unit='t/h')
infos6 = JoinInfos(id='6', name='脱氨喷氨需求量', groupA='22', groupB='0.06', unit='t/h')
infos7 = JoinInfos(id='7', name='沉积系数', groupA='22', groupB='15.6', unit='MW')
infos8 = JoinInfos(id='8', name='沉积系数周均值', groupA='22', groupB='15.6', unit='MW')
db.session.add_all([infos1, infos2, infos3, infos4, infos5, infos6, infos7, infos8])
db.session.commit()

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


@app.route('/api/getdrawPieChart', methods=['GET'])
@auth.login_required
def getdrawPieChart():
    query = db.session.query
    Infos = query(JoinInfos)
    total = Infos.count()
    data_value = [0, 0, 0, 0, 0, 0, 0]  # 和下面组别一一对应
    group_value = ['视觉', '视频', '前端', '办公', '后端', '运营', '移动']
    for info in Infos:
        for num in range(0, 7):
            if group_value[num] in info.group:
                data_value[num] += 1
            else:
                pass
    return jsonify({'code': 200, 'value': data_value, 'total': total})


@app.route('/api/getdrawLineChart', methods=['GET'])
@auth.login_required
def getdrawLineChart():
    grade_value = []  # 年级汇总
    profess_value = []  # 学院汇总
    grade_data = {}  # 年级各学院字典
    Infos = JoinInfos.query.all()
    for info in Infos:
        if info.grade not in grade_value:
            grade_value.append(info.grade)
            grade_data[info.grade] = []
        if info.profess not in profess_value:
            profess_value.append(info.profess)
    for grade in grade_value:
        for profess in profess_value:
            grade_data[grade].append(0)
    for info in Infos:
        for grade in grade_value:
            for profess_local_num in range(0, len(profess_value)):
                if info.profess == profess_value[profess_local_num] and info.grade == grade:
                    grade_data[grade][profess_local_num] += 1
                else:
                    pass
    return jsonify({'code': 200, 'profess_value': profess_value, 'grade_value': grade_value, 'grade_data': grade_data})

# @app.route('/api/getdrawLineChartBlock', methods=['GET'])
# @auth.login_required
# def getdrawLineChartBlock():

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0')