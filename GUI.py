from tkinter import *


class GUI(object):

    def __init__(self):
        self._root = Tk()
        self._root.geometry("1400x900")
        self._root.title("MQTT Client")
        self._button1 = Button(self._root, text="Close", command=self._root.quit)
        self._button1.place(bordermode=OUTSIDE, x=1200, y=800)
        self._root.bind("<Button-1>", self.motion)

        self._root.update()

        self._root.mainloop()

    def motion(self, event):
        print(event.x, event.y)