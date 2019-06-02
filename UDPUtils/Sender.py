from PIL import ImageGrab
import socket
import threading
import time
import zlib
import struct
from utils.ScreenShot import get_screenshot

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
        # self.WIDTH = 640
        # self.HEIGHT = 480
        self.WIDTH = 600
        self.HEIGHT = int(1600//(2560/self.WIDTH))


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
        self.i = 0
        t = 0
        lastTime = 0
        while True:
            # time.sleep(0.01)
            print(self.i)
            lastTime = t
            t = time.time()
            print("fps: ", 1//(t-lastTime))
            self.i += 1
            ttt = time.time()
            image = get_screenshot()
            print(1, time.time()-ttt)
            ttt = time.time()
            image = image.convert("RGB")
            print(2, time.time()-ttt)
            ttt = time.time()
            image.thumbnail((self.WIDTH, self.HEIGHT))
            print(3, time.time() - ttt)
            # image.show()
            # time.sleep(1)
            imageBytes = image.tobytes()
            # imageBytes = compress(imageBytes)
            length = len(imageBytes)
            self.socket.sendto(bytes(str(length), "utf-8"), self.ADDR)
            print(length)
            partLength = 1000

            for i in range(length//partLength+1):
                d = imageBytes[i*partLength:(i+1)*partLength]
                # print(len(d), d)
                l = len(d)
                if len(d)<10000:
                    d += b"\x00"*(1000-len(d))
                message = struct.pack("1000sii", d, i, l)
                self.socket.sendto(message, self.ADDR)
            print("传输完毕")
            self.socket.sendto(b"end", self.ADDR)
            # fhead = struct.pack()
            # self.socket.sendto(imageBytes, self.ADDR)
            time.sleep(1000)

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
        try:
            self.socket.sendto(b"shutdown", self.ADDR)
            self.socket.close()
            time.sleep(0.1)
            super()._stop()
        except:
            pass


# send = Sender()
# send.start()

