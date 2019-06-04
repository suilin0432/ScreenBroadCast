from tkinter import *
from UDPUtils.Receiver import Receiver
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
        self.statusLabel.pack(side = TOP)
        self.connectTopLeft.pack(side = LEFT)
        self.targetInput = Entry(self.connectTopRight)
        self.targetInput.pack(side = TOP)
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
        self.imgId = None
        self.status = "Start"
        self.reInit()
        self.pack()
        self.createWidgets()

    def reInit(self):
        self.re = Receiver(self)
        self.re.start()

    def connect(self):
        print("connect")
        pass

    def destroy(self):
        _async_raise(self.re.ident, SystemExit)
        self.status = "Close"

WIDTH = 600
HEIGHT = int(1600//(2560/WIDTH))

root = Tk()
root.geometry("{0}x{1}".format(WIDTH, HEIGHT))
app = Application(WIDTH, HEIGHT, master=root)
app.mainloop()
root.destroy()