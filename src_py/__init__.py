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
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
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