from tkinter import *
from UDPUtils.Receiver import Receiver
from TCPUtils.TCPClient import TCPClient
import tkinter.messagebox
import threading
import ctypes
import inspect
def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
class Application(Frame):
    def createWidgets(self):
        self.topFm = Frame(height=self.HEIGHT, width=self.WIDTH)

        self.connectFm = Frame(self)
        self.connectTop = Frame(self.connectFm)
        self.connectTopLeft = Frame(self.connectTop)
        self.connectTopRight = Frame(self.connectTop)
        self.targetLabel = Label(self.connectTopLeft, text="目标地址:端口: ")
        self.targetLabel.pack(side = TOP)
        self.statusLabel = Label(self.connectTopLeft, text="连接状态: ")
        self.tokenLabel = Label(self.connectTopLeft, text="连接口令: ")
        self.tokenLabel.pack(side = TOP)
        self.statusLabel.pack(side = TOP)
        self.connectTopLeft.pack(side = LEFT)
        self.targetInput = Entry(self.connectTopRight)
        self.targetInput.insert(0, "127.0.0.1:44445")
        self.targetInput.pack(side = TOP)
        self.token = Entry(self.connectTopRight)
        self.token.pack(side = TOP)
        self.statusVT = StringVar()
        self.statusVT.set("未连接")
        self.status = Label(self.connectTopRight, textvariable=self.statusVT)
        self.status.pack(side = TOP)
        self.connectTopRight.pack(side = LEFT)
        self.connectTop.pack(side = TOP)
        self.connectButton = Button(self.connectFm, text = "连接")
        self.connectButton["fg"] = "red"
        self.connectButton["command"] = self.connect
        self.connectButton.pack(side = TOP)
        self.connectFm.pack(side = TOP)

        self.topFm.__setattr__("-topmost", 1)
        self.img = Label(self.topFm, height=self.HEIGHT, width=self.WIDTH, bg="black")
        self.img.pack()
        self.topFm.pack()

    def __init__(self, WIDTH, HEIGHT, master=None):
        Frame.__init__(self, master)
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.loginClient = None
        self.imgId = None
        self.status = "Start"
        self.re = None
        self.messageTimer = threading.Timer(0.1, self.messageCheck)
        self.messageTimer.start()
        self.messageHas = False
        self.messageTitle = ""
        self.messageContent = ""
        self.messageStop = False
        self.pack()
        self.createWidgets()

    def messageCheck(self):
        if self.messageStop:
            return
        if self.messageHas:
            print("messageCheck: ", self.messageHas)
            tkinter.messagebox.showinfo(self.messageTitle, self.messageContent)
            self.messageHas = False
            self.messageContent = ""
            self.messageTitle = ""
        self.messageTimer = threading.Timer(0.1, self.messageCheck)
        self.messageTimer.start()

    def reInit(self):
        if not self.re:
            self.re = Receiver(self)
            self.re.start()

    def connect(self):
        if not self.loginClient:
            ipPort = self.targetInput.get()
            ip, port = ipPort.split(":")
            self.loginClient = TCPClient(self.token.get(), self, S_HOST=ip, S_PORT=int(port))
            self.connectButton["state"] = "disable"
            self.loginClient.start()
            self.loginClient.connect()
            self.connectButton["state"] = "active"
        else:
            ipPort = self.targetInput.get()
            ip, port = ipPort.split(":")
            self.loginClient.ip = ip
            self.loginClient.port = port
            self.loginClient.token = self.token.get()
            self.connectButton["state"] = "disable"
            self.loginClient.connect()
            self.connectButton["state"] = "active"

    def messageShow(self, title, message):
        print("messageShow: title: {}, message:{}".format(title, message))
        self.messageTitle = title
        self.messageContent = message
        self.messageHas = True
        self.connectButton["state"] = "active"


    def destroy(self):
        self.messageStop = True
        self.status = "Close"

WIDTH = 600
HEIGHT = int(1600//(2560/WIDTH))+200

root = Tk()
root.geometry("{0}x{1}".format(WIDTH, HEIGHT))
app = Application(WIDTH, HEIGHT, master=root)
app.mainloop()
root.destroy()