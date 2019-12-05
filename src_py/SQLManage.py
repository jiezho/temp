#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-11-20
# @Author  : zhoujie

import xlrd
from datetime import datetime
from xlrd import xldate_as_tuple
from flask import Flask, g, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from xlrd import xldate_as_tuple
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from passlib.apps import custom_app_context
import flask_excel as excel
from werkzeug import SharedDataMiddleware
from werkzeug.utils import secure_filename
from __init__ import app, db
import excel2db

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
 
db.drop_all()
db.create_all()

# 添加数据
rdkx_user = Admin(id="8",name="rdkx",password="$5$rounds=535000$9WoOVzcj7Fvi3FsJ$EnhMCR6iPrgkp3G1iulbz5dAw9apErh2UrbyVD6JQP7")
db.session.add(rdkx_user)
db.session.commit()

# ‘登录用户’数据库模型
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

