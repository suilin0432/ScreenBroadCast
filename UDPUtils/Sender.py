from PIL import ImageGrab
import socket
import threading
import time
import zlib

# 截图函数
def grabScreen():
    return ImageGrab.grab()

# 压缩函数
def compress(s):
    return

class Sender(threading.Thread):
    def __init__(self, PORT = 33334):
        self.PORT = PORT

    def run(self):
        self.begin()

    def begin(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET ,socket.SO_BROADCAST, 1)
        self.socket.bind(("", self.PORT))
        self.socket.send("")