import socket
import threading
import time
import zlib
import PIL
from PIL import Image
import tkinter
# 解压
def decompress(b):
    return zlib.decompress(b)

# 字节转图像
def bytesToImg(width, height, b, type="RGBA"):
    img = Image.frombytes("RGBA", (width, height), b)
    return img

class Receiver(threading.Thread):
    def __init__(self, window, PORT = 33333):
        threading.Thread.__init__(self)
        self.PORT = PORT
        self.window = window

    def run(self):
        self.begin()

    def begin(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.bind(("", self.PORT))
        print("客户端创建成功，开始接收数据")
        while True:
            data, addr = self.sock.recvfrom(100)
            print(addr)
            time.sleep(0.1)
            # 如果接受到开始信号就创建窗口
            if data == b"start":
                break
        print("接受到开始信号，发送确认信号")
        self.sock.sendto(b"confirm", addr)

        length = 0
        da = b""
        while True:
            data, addr = self.sock.recvfrom(1000)
            if len(data) > 20:
                print(len(data), addr)
            else:
                print(data, addr)
            if data == b"shutdown":
                break
            if length <= 0:
                try:
                    length = int(data.decode("utf-8"))
                    da = b""
                    print(length)
                except:
                    if len(data)<100:
                        print("hehe: ", data)
            else:
                length -= len(data)
                da += data
                print(length)
                if length <= 0:
                    print("end: ",length)
                    self.screen(da)
                    # threading._start_new_thread(self.screen, tuple(da))

            time.sleep(0.1)
        self.begin()
        # windowThread = threading.Thread(target=self.windowInit)
        # windowThread.start()
        # windowThread.join()
    def screen(self, data):
        imgBytes = decompress(data)
        img = bytesToImg(640, 480, imgBytes)
        try:
            self.window.img.delete(self.window.imgId)
        except:
            pass
        self.window.imgId = self.window.img.create_image(640//2, 480//2, image=img)

