#!/usr/bin/python3
#coding=utf-8
import os
import re
import json
import threading
import time
import socket
import queue
from datetime import datetime
from flask import Flask, g, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
import data2db
from data2db import WorkerThread

hostIP = '127.0.0.1'
exitFlag = 0
BUFSIZE = 1024
encoding = 'utf-8'
# def product(bq):
#     str_tuple = ("Python", "Kotlin", "Swift")
#     for i in range(99999):
#         print(threading.current_thread().name + "生产者准备生产元组元素！")
#         time.sleep(0.2)
#         # 尝试放入元素，如果队列已满，则线程被阻塞
#         bq.put(str_tuple[i % 3])
#         print(threading.current_thread().name \
#             + "生产者生产元组元素完成！")
# def consume(bq):
#     while True:
#         print(threading.current_thread().name + "消费者准备消费元组元素！")
#         time.sleep(0.2)
#         # 尝试取出元素，如果队列已空，则线程被阻塞
#         t = bq.get()
#         print(threading.current_thread().name \
#             + "消费者消费[ %s ]元素完成！" % t)

# a read thread, read data from remote
class Reader(threading.Thread):
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client
        
    def run(self):
        while True:
            data = self.client.recv(BUFSIZE)
            if(data):
                string = bytes.decode(data, encoding)
                print(string, end='')
            else:
                break
        print("close:", self.client.getpeername())
        
    # def readline(self):
    #     rec = self.inputs.readline()
    #     if rec:
    #         string = bytes.decode(rec, encoding)
    #         if len(string)>2:
    #             string = string[0:-2]
    #         else:
    #             string = ' '
    #     else:
    #         string = False
    #     return string
 
# a listen thread, listen remote connect
# when a remote machine request to connect, it will create a read thread to handle
class Listener(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.sock.bind(("0.0.0.0", port))
        self.sock.bind(("127.0.0.1", 10000))
        self.sock.listen(5)
    def run(self):
        print("listener started")
        while True:
            client, cltadd = self.sock.accept()
            try:
                client.settimeout(50)
                # Reader(client).start()
                w = WorkerThread(client)
                w.start()
                w.receiveData(BUFSIZE,client)
                # WorkerThread(client).receiveData(client)
                # w.start()
                # w.send("hahahahah")
                # test.WorkerThread(client).receiveData("Listener Receive",client)
                # test.WorkerThread(client).receiveData()
                cltadd = cltadd
                print("accept a connect")
            except socket.timeout: #如果建立连接后，该连接在设定的时间内无数据发来，则time out
                print('time out')
            

class socketThread (threading.Thread):
    def __init__(self, threadID, name, counter, port):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.port = port

    def run(self):
        print ("开启线程： " + self.name)
        # 获取锁，用于线程同步
        threadLock.acquire()
        address = (hostIP,10000)#本主机IP
        readdr = ('127.0.0.1',10001)#客户端主机IP
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(address)
        reciveFlag = 0
        listReceive = []
        while 1:
            data,addr=s.recvfrom(2048)
            if not data:
                break
            print("got data from",addr)
            print(data.decode())
        s.close()
        # 释放锁，开启下一个线程
        threadLock.release()

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print ("开启线程： " + self.name)
        # 获取锁，用于线程同步
        threadLock.acquire()
        print_time(self.name, self.counter, 300)
        # 释放锁，开启下一个线程
        threadLock.release()

def print_time(threadName, delay, counter):
    while counter:
        time.sleep(delay)
        print ("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1

#两秒执行一次
def printHello():
    print('TimeNow:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    t = threading.Timer(2, printHello)
    t.start()

threadLock = threading.Lock()
threads = []

# 创建新线程实例
# thread1 = myThread(1, "Thread-1", 1)
# thread2 = myThread(2, "Thread-2", 2)
# thread3 = socketThread(3, "SocketThread", 30, 10000)
lstThread  = Listener(10000)   # create a listen thread
# w = WorkerThread(Listener.client)

# 开启新线程
# thread1.start()
# thread2.start()
# thread3.start()
lstThread.start() # then start
# w.start()

# 添加线程到线程列表
# threads.append(thread1)
# threads.append(thread2)
# threads.append(thread3)
threads.append(lstThread)
# threads.append(w)

# 等待所有线程完成
for t in threads:
    t.join()
print ("退出主线程")