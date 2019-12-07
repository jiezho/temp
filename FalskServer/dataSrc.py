#coding=utf-8
import socket
import time
import xlrd
import queue
import json
import os
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

addr = ('127.0.0.1',10000)#目标主机IP
readdr = ('127.0.0.1',10001)#本主机IP
# s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# s.bind(readdr)

dataPath = './static/excel'
runtimeData = xlrd.open_workbook(dataPath+'/焦作数据.xlsx')
sheet = runtimeData.sheet_by_name('runtimeDatas')
table = runtimeData.sheet_by_name(u'runtimeDatas')
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
titlelist = list[0]
print(titlelist)
print(list[2][0])
del list[0] # 删掉第一行，第一行获取的是文件的头，一般不用插到数据库里面
q1 = queue.Queue()

for row in range(sheet.nrows - 1):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # SOCK_STREAM设置为TCP
    # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # s.bind(readdr)
    # s = socket.socket()
    s.connect(addr)
    print("建立第%d连接" % (row+1))
    for col in range(sheet.ncols):
        # s.sendto(str(list[row][col]).encode("utf-8"), addr)
        srcData = "rc"+(str(row)+str(col)+"data"+str(list[row][col]))
        s.send(srcData.encode("utf-8"))
        print("send data list[%d][%d]:" % (row, col),list[row][col])
        time.sleep(1)
    s.close()
    print("第%d次连接发送完成，关闭连接" % (row+1))
    time.sleep(2)
