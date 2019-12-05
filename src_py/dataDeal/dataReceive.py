from datetime import datetime
from threading import Timer
import time
import socket

address = ('127.0.0.1',10000)#本主机IP
readdr = ('127.0.0.1',10001)#客户端主机IP
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srcdata = [11,2,33,44,55,6,67,888,22]
s.bind(address)
reciveFlag = 0
listReceive = []
while 1:
    data,addr=s.recvfrom(2048)
    if not data:
        break
    print("got data from",addr)
    print(data.decode())
    # replydata = input("reply:")
    # for data in srcdata:
    #     s.sendto(data,readdr)
    #     print("send data:",data)
    # s.sendto(replydata.encode("utf-8"),readdr)
s.close()
'''
每个 10 秒打印当前时间。
'''
def timedTask():
    '''
    第一个参数: 延迟多长时间执行任务(单位: 秒)
    第二个参数: 要执行的任务, 即函数
    第三个参数: 调用函数的参数(tuple)
    '''
    Timer(10, task, ()).start()

# 定时任务
def task():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == '__main__':
    timedTask()
    while True:
        print(time.time())
        time.sleep(5)