from PIL import ImageGrab
import socket
import threading
import time
import zlib
import struct

# 截图函数
def grabScreen():
    return ImageGrab.grab()

# 压缩函数
def compress(s):
    return zlib.compress(s)

class Sender(threading.Thread):
    def __init__(self, window, PORT = 33334, SEND_PORT = 33333):
        threading.Thread.__init__(self)
        self.window = window
        self.PORT = PORT
        self.HOST = "<broadcast>"
        self.SEND_PORT = SEND_PORT
        self.ADDR = (self.HOST, self.SEND_PORT)
        self.state = "starting"
        self.window.stateVT.set(self.state)
        self.WIDTH = 640
        self.HEIGHT = 480


    def run(self):
        self.begin()

    def begin(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET ,socket.SO_BROADCAST, 1)
        self.socket.bind(("", self.PORT))
        print("服务器创建成功，开始发送数据")
        threading._start_new_thread(self.waitConfirm, ())
        while True:
            print("send start")
            self.socket.sendto(b"start", self.ADDR)
            if self.state == "sending":
                break
            time.sleep(1)
        print("接受到确认信号, 开始进行图片发送")

        self.screenSending()

    def screenSending(self):
        while True:
            time.sleep(5)
            image = ImageGrab.grab()
            image = image.resize((self.WIDTH, self.HEIGHT))
            imageBytes = image.tobytes()
            imageBytes = compress(imageBytes)
            length = len(imageBytes)
            self.socket.sendto(bytes(str(length), "utf-8"), self.ADDR)
            print(length)
            for i in range(length//1000+1):
                self.socket.sendto(imageBytes[i*1000:(i+1)*1000], self.ADDR)
                time.sleep(0.2)
            # fhead = struct.pack()
            # self.socket.sendto(imageBytes, self.ADDR)


    def waitConfirm(self):
        while True:
            data, addr = self.socket.recvfrom(100)
            print(data, addr)
            if data == b"confirm":
                self.state = "sending"
                self.window.stateVT.set(self.state)
                break

    def _stop(self):
        print(111)
        self.socket.sendto(b"shutdown", self.ADDR)
        time.sleep(0.1)
        super()._stop()

# send = Sender()
# send.start()

