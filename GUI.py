from tkinter import *
from client import *


class GUI(object):

    def __init__(self):
        self.__root = Tk()
        self.__root.geometry("1400x900")
        self.__root.title("MQTT Client")

        self.__button_quit = Button(self.__root, text="Quit", command=self.__root.quit)
        self.__button_quit.place(bordermode=OUTSIDE, x=1200, y=800)

        def motion(event):
            print(event.x, event.y)

        self.__root.bind("<Button-1>", motion)

        self.__label_username = Label(self.__root, text='Username').place(x=500, y=300)
        self.__entry_username = Entry(self.__root)
        self.__entry_username.focus_set()
        self.__entry_username.place(x=590, y=300)

        self.__label_password = Label(self.__root, text='Password').place(x=500, y=330)
        self.__entry_password = Entry(self.__root, show='*')
        self.__entry_password.place(x=590, y=330)

        def callback():
            # Create a client object when the connect button is pressed
            self.__client = Client(1, username=self.__entry_username.get(), password=self.__entry_password.get())
            self.__client.connect()

        self.__button_connect = Button(self.__root, text="Connect", width=10, command=callback)
        self.__button_connect.place(x=600, y=400)

        self.__root.update()
        self.__root.mainloop()

