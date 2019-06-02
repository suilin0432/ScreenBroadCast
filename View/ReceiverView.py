from tkinter import *
from UDPUtils.Receiver import Receiver
import threading

class Application(Frame):
    def createWidgets(self):
        self.topFm = Frame(self)
        self.topFm.__setattr__("-topmost", 1)
        self.img = Canvas(self.topFm, bg="white")
        self.img.create_image()
        self.img.pack()
        self.topFm.pack()

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.imgId = None
        self.reInit()
        self.pack()
        self.createWidgets()

    def reInit(self):
        re = Receiver(self)
        re.start()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()