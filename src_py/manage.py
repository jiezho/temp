#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-11-20
# @Author  : zhoujie

import os
import re
import json
import xlrd

from datetime import datetime
from xlrd import xldate_as_tuple
from flask import Flask, g, jsonify, make_response, request
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from passlib.apps import custom_app_context
import flask_excel as excel
from werkzeug import SharedDataMiddleware
from werkzeug.utils import secure_filename

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# r'/*' 是通配符，让本服务器所有的 URL 都允许跨域请求
# cors = CORS(app, resources={r"/*": {"origins": "*"})
# CORS(app, resources=r'/*')
CORS(app, supports_credentials=True)

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
    groupA = db.Column(db.Float)
    groupB = db.Column(db.Float)
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
 
# 创建excel导入的runtime数据数据库模型
class HistoryData(db.Model):
    __tablename__ = 'historyDatas'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.DateTime, default=datetime.now())
    airClogA = db.Column(db.Float)
    airClogB = db.Column(db.Float)
    sizeNH3Actual = db.Column(db.Float)
    sizeNH3Demand = db.Column(db.Float)
    airDeposiA = db.Column(db.Float)
    airDeposiB = db.Column(db.Float)

    def to_dict(self):
        columns = self.__table__.columns.keys()
        result = {}
        for key in columns:
            if key == 'time':
                value = getattr(self, key).strftime("%Y-%m-%d %H:%M:%S")
            else:
                value = getattr(self, key)
            result[key] = value
        return result
    
db.drop_all()
db.create_all()

# 添加数据
rdkx_user = Admin(id="8",name="rdkx",password="$5$rounds=535000$9WoOVzcj7Fvi3FsJ$EnhMCR6iPrgkp3G1iulbz5dAw9apErh2UrbyVD6JQP7")
db.session.add(rdkx_user)
db.session.commit()

infos1 = JoinInfos(id='1', name='机组负荷', groupA='421.88', groupB='421.88', unit='MW')
infos2 = JoinInfos(id='2', name='烟气侧压差', groupA='1100', groupB='930', unit='Pa')
infos3 = JoinInfos(id='3', name='堵塞系数', groupA='1.248', groupB='1.055', unit='')
infos4 = JoinInfos(id='4', name='堵塞速度', groupA='-11.04', groupB='-4.12', unit='%/天')
infos5 = JoinInfos(id='5', name='脱硝实际喷氨量', groupA='103.26', groupB='105.37', unit='kg/h')
infos6 = JoinInfos(id='6', name='脱氨喷氨需求量', groupA='84.35', groupB='84.35', unit='kg/h')
infos7 = JoinInfos(id='7', name='沉积系数', groupA='62334', groupB='60891', unit='')
infos8 = JoinInfos(id='8', name='沉积系数12天均值', groupA='73776', groupB='70818', unit='')
db.session.add_all([infos1, infos2, infos3, infos4, infos5, infos6, infos7, infos8])
db.session.commit()

# excel数据导入到数据库
dataPath = '../src/data/excel'
runtimeData = xlrd.open_workbook(dataPath+'/焦作数据.xlsx')
sheet = runtimeData.sheet_by_name('historyData')
table = runtimeData.sheet_by_name(u'historyData')
list = []
for row in range(sheet.nrows):
    rowlist = []
    for col in range(sheet.ncols):
        value = sheet.cell(row,col).value        
        if sheet.cell(row,col).ctype == 3:            
            date = xldate_as_tuple(sheet.cell(row,col).value,0)            
            value = datetime(*date)  # excel中读取时间格式数据要注意      
            # print('value',value)
        rowlist.append(value)
    list.append(rowlist)

del list[0] #删掉第一行，第一行获取的是文件的头，一般不用插到数据库里面
# print('list', list)
    # 将数据存入数据库
for a in list:
    historydatas = HistoryData()
    historydatas.id = a[0]
    # historydatas.time = a[1].to_dict()
    historydatas.time = a[1]
    # print('historydatas.time',historydatas.time)
    historydatas.airClogA = a[2]
    historydatas.airClogB = a[3]
    historydatas.sizeNH3Actual = a[4]
    historydatas.sizeNH3Demand = a[5]
    historydatas.airDeposiA = a[6]
    historydatas.airDeposiB = a[7]
    # print('list a',historydatas)
    db.session.add(historydatas)
    db.session.commit()
print(list[3][1])

listAirClogA = []
listAirClogB = []
listSizeNH3Actual = []
listSizeNH3Demand = []
listAirDeposiA = []
listAirDeposiB = []

for row in range(sheet.nrows - 1):
    listAirClogA.append({0:list[row][1], 1:list[row][2]})
    listAirClogB.append({0:list[row][1], 1:list[row][3]})
    listSizeNH3Actual.append({0:list[row][1], 1:list[row][4]})
    listSizeNH3Demand.append({0:list[row][1], 1:list[row][5]})
    listAirDeposiA.append({0:list[row][1], 1:list[row][6]})
    listAirDeposiB.append({0:list[row][1], 1:list[row][7]})

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

# excel数据交互(还是没成功)
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