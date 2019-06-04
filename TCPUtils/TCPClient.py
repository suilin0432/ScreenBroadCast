import socket
import collections
from chardet import detect
import threading
import time
import os

class TCPClient(threading.Thread):
    def __init__(self, token, window, S_HOST="127.0.0.1", S_PORT=44445, C_HOST="127.0.0.1", C_PORT=44446, maxNumber = 1):
        threading.Thread.__init__(self)
        self.token = token
        self.window = window
        self.S_HOST = S_HOST
        self.S_PORT = S_PORT
        self.C_HOST = C_HOST
        self.C_PORT = C_PORT
        self.maxNumber = maxNumber
        self.STATUS = False
        self.HAS = True
        socket.setdefaulttimeout(0.3)

    def run(self):
        while self.HAS:
            time.sleep(5)

    def stop(self):
        self.HAS = False

    def connect(self):
        S_ADDR = (self.S_HOST, self.S_PORT)
        C_ADDR = (self.C_HOST, self.C_PORT)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client.bind(C_ADDR)
        print(S_ADDR)
        try:
            self.client.connect(S_ADDR)
        except:
            # try:
            self.window.messageShow("提示", "连接失败")
            self.window.messageHas = True
            # except:
            #     pass
            try:
                self.client.shutdown(socket.SHUT_RDWR)
            except:
                print("SHUTDOWN ERROR")
            self.client.close()
            return


        # 发送一个 token, 然后等待消息的接受，如果接受 success 显示成功 然后设置状态为连接成功 fail 显示登陆失败
        self.client.send(bytes("token:{0}".format(self.token), "utf-8"))
        msg = self.client.recv(1000)
        if msg == b"success":
            print("登陆成功")
            self.window.messageShow('提示', '登陆成功')
            self.window.statusVT.set("已连接")
            self.STATUS = True
            self.window.reInit()
        else:
            print("登陆失败")
            self.window.messageShow("提示", "登陆失败")
        try:
            self.client.shutdown(socket.SHUT_RDWR)
        except:
            print("SHUTDOWN ERROR")
        self.client.close()
