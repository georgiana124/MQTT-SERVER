from tkinter import *


class GUI(object):

    def __init__(self):
        root = Tk()

        w = Canvas(root, width=1400, height=900)
        w.pack()
        root.update()
        mainloop()


