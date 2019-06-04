import socket
import collections
from chardet import detect
import threading
import time

class TCPServer(threading.Thread):
    def __init__(self, window, token="none", HOST = "127.0.0.1", PORT = 44445, maxNumber = 100):
        threading.Thread.__init__(self)
        # self.token = bytes(token, "utf-8")
        self.window = window
        self.token = token
        self.HOST = HOST
        self.PORT = PORT
        self.ADDR = (HOST, PORT)
        self.STOP = True
        # 最大同时连接数
        self.maxNumber = maxNumber

    def run(self):
        self.listen()

    def stop(self):
        self.window.tcp = None
        self.STOP = False
        try:
            self.tcpServiceSock.shutdown(socket.SHUT_RDWR)
        except:
            print("shutdown wrong")
        self.tcpServiceSock.close()

    def listen(self):
        # AF_INET 表示 针对 IPV4
        # SOCK_STREAM 表示针对 面向流的TCP协议
        self.tcpServiceSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpServiceSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcpServiceSock.bind(self.ADDR)
        self.tcpServiceSock.listen(self.maxNumber)
        while self.STOP:
            # print("等待连接")
            client, addr = self.tcpServiceSock.accept()
            # print("已经和 {0} 产生了连接, 可以开始通话了!!".format(addr))
            self.connectEvent(client, addr)

    def connectEvent(self, client, addr):
        message = client.recv(1000)
        if not self.window.se:
            client.send(b"false")
            return
        print(message, self.token)
        message = message.decode("utf-8").split("token:")[-1]
        if message == self.token:
            client.send(b"success")
        else:
            client.send(b"false")
        client.close()