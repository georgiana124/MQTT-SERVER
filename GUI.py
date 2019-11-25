from tkinter import *
from client import *


class GUI(object):

    def __init__(self):
        self.__root = Tk()
        self.__root.geometry("1400x900")
        self.__root.title("MQTT Client")
        self.__button1 = Button(self.__root, text="Close", command=self.__root.quit)
        self.__button1.place(bordermode=OUTSIDE, x=1200, y=800)

        def motion(event):
            print(event.x, event.y)

        self.__root.bind("<Button-1>", motion)

        Label(self.__root, text='Username').place(x=500, y=300)
        e1 = Entry(self.__root)
        e1.focus_set()

        e1.place(x=590, y=300)

        def callback():
            # Create a client object when the connect button is pressed
            self.__client = Client(e1.get(), e2.get())

        Label(self.__root, text='Password').place(x=500, y=330)
        e2 = Entry(self.__root)
        e2.place(x=590, y=330)

        b = Button(self.__root, text="Connect", width=10, command=callback)
        b.place(x=600, y=400)
        self.__root.update()
        self.__root.mainloop()

