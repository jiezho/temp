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

# class ExcelClass(path):
#     def readExcel(self, sheet):
#         list = []
#         return list

# 创建excel导入的History数据数据库模型
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

    
db.drop_all()
db.create_all()

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
