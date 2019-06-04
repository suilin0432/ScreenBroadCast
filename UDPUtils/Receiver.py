import socket
import threading
import time
import zlib
import PIL
import struct
from PIL import Image, ImageTk
import tkinter
# 解压
def decompress(b):
    return zlib.decompress(b)

# 字节转图像
def bytesToImg(width, height, b, type="RGBA"):
    img = Image.frombytes("RGB", (width, height), b)
    return img

class Receiver(threading.Thread):
    def __init__(self, window, PORT = 33333):
        threading.Thread.__init__(self)
        self.i = 0
        self.PORT = PORT
        self.window = window
        # self.WIDTH = 640
        # self.HEIGHT = 480
        self.WIDTH = 600
        self.HEIGHT = int(1600//(2560/self.WIDTH))
        self.timer = threading.Timer(1, self.windowStatus)
        self.timer.start()

    def windowStatus(self):
        print("timer: ", self.window.status)
        if self.window.status == "Close":
            self.sock.close()
        else:
            self.timer = threading.Timer(1, self.windowStatus)
            self.timer.start()

    def run(self):
        self.begin()



    def begin(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.bind(("", self.PORT))
        print("客户端创建成功，开始接收数据")
        while True:
            data, addr = self.sock.recvfrom(50000)
            print(addr)
            time.sleep(0.1)
            # 如果接受到开始信号就创建窗口
            if data == b"start":
                break
        print("接受到开始信号，发送确认信号")
        self.sock.sendto(b"confirm", addr)

        length = 0
        da = []
        partLength = 1464
        base = b"\x00" * partLength
        while True:
            data, addr = self.sock.recvfrom(50000)
            if len(data) > 20:
                pass
                # print(len(data), addr)
            else:
                print(data, addr)
            if data == b"shutdown":
                break
            if data == b"end":
                length = 0
                self.screen(da)
                continue
            try:
                if length <= 0:
                    try:
                        length = int(data.decode("utf-8"))
                        da = [base for _ in range(length//partLength+1)]
                        da[-1]=b"\x00"*(length%partLength)
                        # print(length)
                    except:
                        if len(data)<100:
                            print("hehe: ", data)
                else:
                    # print(len(data))
                    dat, l, valid = struct.unpack("{0}sii".format(partLength), data)
                    # print(l)
                    length -= len(data)-8
                    # da += data
                    da[l] = dat[:valid]
                    # print(length)
                        # threading._start_new_thread(self.screen, tuple(da))
            except:
                length = 0
                self.screen(da)

            # time.sleep(0.1)
        self.begin()
        # windowThread = threading.Thread(target=self.windowInit)
        # windowThread.start()
        # windowThread.join()
    def screen(self, data):
        # print(self.i)
        self.i += 1
        da = b""
        for index, i in enumerate(data):
            # print(index, len(i))
            da += i
        print("screen: ", len(da))
        # imgBytes = decompress(data)
        try:
            img = bytesToImg(self.WIDTH, self.HEIGHT, da)
            img = ImageTk.PhotoImage(img)
            print("fill", img.height(), img.width())
            self.window.img.config(image=img)
            self.window.img.image = img
        except:
            pass

