from tkinter import *
from Client import *


class GUI:

    def __init__(self):
        self.__root = Tk()  # Create the main root for the app
        self.__width = 800
        self.__height = 500
        # Create a root app based on the width and height defined
        self.__root.geometry(str(self.__width) + "x" + str(self.__height))
        self.__root.title("MQTT Client")
        self.__label_username = Label(self.__root, text='Username')
        self.__entry_username = Entry(self.__root)
        self.__label_password = Label(self.__root, text='Password')
        self.__entry_password = Entry(self.__root, show='*')
        self.__button_quit = Button(self.__root, text="Quit", command=self.__root.quit)
        self.__entry_topic = Entry(self.__root)
        self.__label_topic = Label(self.__root, text='Topic')
        self.__text_box_receive = Text(self.__root, width=50, height=10)
        self.__text_box_send = Text(self.__root, width=50, height=10)

        def send_callback():
            pass

        def connect_button_callback():
            self.__client = Client("123", username=self.__entry_username.get(), password=self.__entry_password.get())  # Create a client object when the connect button is pressed
            self.__client.connect()
            if self.__client.get_is_connected() is True:
                """If we successfully connect to the broker
                 we dispose the tkinter objects in the root and create the next state"""
                self.dispose_connect_gui()
                self.create_main_gui()

        self.__button_send = Button(self.__root, text="Send", command=send_callback)
        self.__button_connect = Button(self.__root, text="Connect", width=10, command=connect_button_callback)
        self.create_connect_gui()

    def run(self):
        self.__root.mainloop()

    def create_connect_gui(self):
        def motion(event):  # A motion callback function
            print(event.x, event.y)

        self.__button_quit.place(bordermode=OUTSIDE, x=self.__width / 10 * 9, y=self.__height / 10 * 9)
        self.__root.bind("<Button-1>", motion)  # Bind the motion function to be called whenever the left click is pressed
        self.__label_username.place(x=self.__width / 3, y=self.__height / 5)
        self.__entry_username.focus_set()
        self.__entry_username.place(x=self.__width / 3 + 90, y=self.__height / 5)
        self.__label_password.place(x=self.__width / 3, y=self.__height / 5 + 30)
        self.__entry_password.place(x=self.__width / 3 + 90, y=self.__height / 5 + 30)
        self.__button_connect.place(x=self.__width / 3 + 100, y=self.__height / 5 + 100)

    def dispose_connect_gui(self):
        self.__label_username.place_forget()
        self.__label_password.place_forget()
        self.__entry_password.place_forget()
        self.__entry_username.place_forget()
        self.__button_connect.place_forget()
        self.__root.update()

    def create_main_gui(self):
        self.__entry_topic.place(x=self.__width/8, y=self.__height/7)
        self.__button_send.place(bordermode=OUTSIDE, x=self.__width/8+45, y=self.__height/7+30)
        self.__label_topic.place(x=self.__width/8-60, y=self.__height/7)
        self.__text_box_receive.place(x=self.__width/5*2, y=self.__height/7)

    def dispose_main_gui(self):
        self.__entry_topic.place_forget()
        self.__button_send.place_forget()
        self.__label_topic.place_forget()
