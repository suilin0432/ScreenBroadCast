from tkinter import *
from UDPUtils.Sender import Sender
from TCPUtils.TCPServer import TCPServer
import threading
import os

class Application(Frame):
    def createWidgets(self):

        self.TOKEN = "none"
        self.topFm = Frame(self)
        self.tokenLabel = Label(self.topFm, text="token: ")
        self.tokenLabel.pack(side = LEFT)
        self.token = Entry(self.topFm)
        self.token.pack(side = LEFT)
        self.setButton = Button(self.topFm, text="设置")
        self.setButton["fg"] = "red"
        self.setButton["command"] = self.tokenSet
        self.setButton.pack(side = LEFT)
        self.topFm.pack(side = TOP)

        self.buttonFm = Frame(self)
        self.startButton = Button(self.buttonFm, text="start")
        self.startButton["fg"] = "red"
        self.startButton["command"] = self.seStart
        self.startButton.pack(side = LEFT)
        self.endButton = Button(self.buttonFm, text="stop")
        self.endButton["fg"] = "red"
        self.endButton["command"] = self.seEnd
        self.endButton["state"] = "disable"
        self.endButton.pack(side = LEFT)
        self.buttonFm.pack(side = TOP)
        self.stateFm = Frame(self)
        self.stateVT = StringVar()
        self.stateVT.set("未连接")
        self.stateL = Label(self.stateFm, text="连接状态: ")
        self.stateL.pack(side = LEFT)
        self.stateLabel = Label(self.stateFm, textvariable=self.stateVT)
        self.stateLabel.pack(side = LEFT)
        self.stateFm.pack(side = TOP)
        self.senderThread = None

    def seStart(self):
        # self.senderThread = threading.Thread(target=self.seInit)
        self.startButton["state"] = "disable"
        self.endButton["state"] = "active"
        self.seInit()
        # self.senderThread.start()

    def seEnd(self):
        self.se.stop()
        self.tcp.stop()
        self.stateVT.set("未连接")
        self.setButton["state"] = "active"
        self.startButton["state"] = "active"
        self.endButton["state"] = "disable"

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.tcp = None
        self.se = None
        self.pack()
        self.createWidgets()

    def killport(self, port):
        command = '''kill -9 $(netstat -nlp | grep :''' + str(
            port) + ''' | awk '{print $7}' | awk -F"/" '{ print $1 }')'''
        print(command)
        os.system(command)

    def seInit(self):
        if not self.se:
            self.se = Sender(self)
            self.se.start()
        if not self.tcp:
            self.tcp = TCPServer(self, token=self.TOKEN)
            self.tcp.start()
        self.tcp.token=self.TOKEN
        self.setButton["state"] = "disable"

    def tokenSet(self):
        self.TOKEN = self.token.get()

    def destroy(self):
        self.tcp.stop()
        self.se.stop()
        super().destroy()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()