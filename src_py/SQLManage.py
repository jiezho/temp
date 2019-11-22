#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-11-20
# @Author  : zhoujie

import os
import re
import json
import pymysql
from datetime import datetime

from flask import Flask, g, jsonify, make_response, request
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
 
# 配置不变: 后期可以放在配置文件中
HOSTNAME = 'localhost'
PORT = '3306'
DATABASE = 'rdkx'
USERNAME = 'root'
PASSWORD = '000000'
DB_URI = "mysql+pymysql://{}:{}@{}:{}/{}".format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
 
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
# 下面这个设置，请自己查，老师遇到了，自己写的没有遇到，估计是版本问题。
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
 
# 创建ORM模型
class Data(db.Model):
    __tablename__ = 'data'
    # 因为封装了，所以不用单独再导入Column、Integer等等
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dataName = db.Column(db.String(50))
 
    def __repr__(self):
        return "<Data:%s>"%self.dataName
 
class Article(db.Model):
    __tablename__ = "article"
 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    # 定义外键
    uid = db.Column(db.Integer, db.ForeignKey("data.id"), nullable=False)
 
    author = db.relationship("Data", backref="articles")

class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True)
    password = db.Column(db.String(128))

# 将模型映射到数据库中
db.drop_all()
db.create_all()
 
# 添加数据
data = Data(dataName="cc")
article = Article(title="luluxiu")
article.author = data
db.session.add(article)
db.session.commit()

rdkx_user = Admin(id="8",name="rdkx",password="$5$rounds=FsJ$EnhMCR6i")
db.session.add(rdkx_user)
db.session.commit()


# 查找数据
# User.query 和 db.session.query(User)效果一样
datas = Data.query.all() # 返回list
print(datas)

admins = Admin.query.all()
print('admin',admins)
# 排序: users = User.query.order_by(User.id.desc()).all()
# 其他                    .filter
                        # .filter_by
                        # .group_by
                        # .join
 
# 修改
data = Data.query.filter(Data.dataName=="cc").first()
Data.dataName = 'gg'
db.session.commit()
 
# 删除
article = Article.query.first()
db.session.delete(article)
db.session.commit()
 
@app.route("/")
def index():
    return 'hello world'
 
if __name__ == "__main__":
    app.run()