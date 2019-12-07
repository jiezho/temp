from threading import Thread
import threading
from queue import Queue
import os
import re
import json
import time
import socket
from datetime import datetime
from flask import Flask, g, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy

hostIP = '127.0.0.1'
exitFlag = 0
encoding = 'utf-8'
BUFSIZE = 1024

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
# 创建实时数据数据库
class RuntimeDatas(db.Model):
    __tablename__ = 'runtimeData'
    # prepare_list = locals()
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.DateTime, default=datetime.now())
    # for i in range(12):
    #     prepare_list['Col'+str(i+1)] = db.Column(db.Float)
    Col1 = db.Column(db.Float)
    Col2 = db.Column(db.Float)
    Col3 = db.Column(db.Float)
    Col4 = db.Column(db.Float)
    Col5 = db.Column(db.Float)
    Col6 = db.Column(db.Float)
    Col7 = db.Column(db.Float)
    Col8 = db.Column(db.Float)
    Col9 = db.Column(db.Float)
    Col10 = db.Column(db.Float)
    Col11 = db.Column(db.Float)
    Col12 = db.Column(db.Float)
    Col13 = db.Column(db.Float)
    Col14 = db.Column(db.Float)

db.drop_all()    # 删除所有表
db.create_all()  # 创建所有表

class WorkerThread(Thread):
    def __init__(self, client):
        Thread.__init__(self)
        self.input_queue=Queue(100)
        self.client = client

    def receiveData(self,BUFSIZE,client):
        while True:
            data = self.client.recv(BUFSIZE)
            if(data):
                string = bytes.decode(data, encoding)
                print("receiveData",string, end='\n')
                self.input_queue.put(data)
            else:
                break
        print("close:", self.client.getpeername())
        # self.input_queue.put(data)
        print('quene size', self.input_queue.qsize())
        print('quene empty?', self.input_queue.empty())
        print('quene full?', self.input_queue.full())
    def close(self):
        self.input_queue.put(None)
        print("workerThread close")
        self.input_queue.join()
    def run(self):
        while True:
            queueData=self.input_queue.get()
            if queueData is None:
                break
            #实际开发中，此处应该使用有用的工作代替
            print("deal received data",queueData)
            if queueData[3:3] == 0:
                runtime_data = RuntimeDatas(id = queueData[2:2], time = queueData[8:])
            elif queueData[3:3] == 1:
                runtime_data = RuntimeDatas(id = queueData[2:2], Co1 = queueData[8:])
            elif queueData[3:3] == 2:
                runtime_data = RuntimeDatas(id = queueData[2:2], Co2 = queueData[8:])
            else:
                break
            print("runtime_data",runtime_data)
            db.session.add(runtime_data)
            db.session.commit()
            self.input_queue.task_done()
        #完成，指示收到和返回哨兵
        self.input_queue.task_done()
        return

# if __name__=="__main__":
#     w=WorkerThread()
#     w.start()
#     w.send("Mark")
#     w.send("好")
#     w.send("TM")
#     w.send("帅")
#     w.close()
