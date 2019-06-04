from tkinter import *
from UDPUtils.Sender import Sender
import threading

class Application(Frame):
    def createWidgets(self):

        self.buttonFm = Frame(self)
        self.startButton = Button(self.buttonFm, text="start")
        self.startButton["fg"] = "red"
        self.startButton["command"] = self.seStart
        self.startButton.pack(side = LEFT)
        self.endButton = Button(self.buttonFm, text="stop")
        self.endButton["fg"] = "red"
        self.endButton["command"] = self.seEnd
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
        self.seInit()
        # self.senderThread.start()

    def seEnd(self):
        self.se._stop()
        self.stateVT.set("未连接")

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def seInit(self):
        self.se = Sender(self)
        self.se.start()


root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()