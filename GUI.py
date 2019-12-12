from tkinter import *
from Client import *


class GUI:

    def __init__(self):
        # Create the main root for the app
        self.__root = Tk()
        self.__width = 1400
        self.__height = 900
        # Create a root app based on the width and height defined
        self.__root.geometry(str(self.__width) + "x" + str(self.__height))
        self.__root.title("MQTT Client")

        self.__button_quit = Button(self.__root, text="Quit", command=self.__root.quit)
        self.__button_quit.place(bordermode=OUTSIDE, x=self.__width/15*14, y=self.__height/15*14)

        # A motion callback function
        def motion(event):
            print(event.x, event.y)

        # Bind the motion function to be called whenever the left click is pressed
        self.__root.bind("<Button-1>", motion)

        self.__label_username = Label(self.__root, text='Username').place(x=500, y=300)
        self.__entry_username = Entry(self.__root)
        self.__entry_username.focus_set()
        self.__entry_username.place(x=590, y=300)

        self.__label_password = Label(self.__root, text='Password').place(x=500, y=330)
        self.__entry_password = Entry(self.__root, show='*')
        self.__entry_password.place(x=590, y=330)

        def connect_button_callback():
            # Create a client object when the connect button is pressed
            self.__client = Client("123", username=self.__entry_username.get(), password=self.__entry_password.get())
            self.__client.connect()
            if self.__client.get_is_connected() is True:
                # If we successfully connect to the broker we dispose the tkinter objects in the root and create the next state
                self.dispose()

        self.__button_connect = Button(self.__root, text="Connect", width=10, command=connect_button_callback)
        self.__button_connect.place(x=600, y=400)

    def run(self):
        self.__root.mainloop()

    def dispose(self):
        self.__button_quit.place_forget()
        self.__label_password.place_forget()
        self.__label_username.place_forget()
        self.__root.update()
