import socket
import threading
import time
import zlib
import PIL
# 解压
def decompress(b):
    return zlib.decompress(b)

# 字节转图像
def bytesToImg(height, width, b, type="RGBA"):
    img = PIL.Image.frombytes("RGBA", (height, width), b)
    return img

class Receiver(threading.Thread):
    def __init__(self, PORT = 33333):
        self.PORT = PORT

    def run(self):
        self.begin()

    def begin(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.bind(("", self.PORT))
        while True:
            data, addr = self.sock.recvfrom(100)
        # 接受到服务器发送的开始广播指令

        self.sock.close()

