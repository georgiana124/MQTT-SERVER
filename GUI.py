from tkinter import *
from Client import *

""" The GUI class handles the front end of the app: what does the user see.
    It uses tkinter and contains all the graphical elements. """
class GUI:

    def __init__(self):
        self.__client = None
        self.__root = Tk()  # Create the main root for the app
        self.__width = 1400
        self.__height = 800

        """ Create a root app based on the width and height defined """
        self.__root.geometry(str(self.__width) + "x" + str(self.__height))
        self.__root.title("MQTT Client")

        """ Create the gui labels """
        self.__label_username = Label(self.__root, text='Username')
        self.__label_password = Label(self.__root, text='Password')
        self.__label_receive_message = Label(self.__root, text='Received message')
        self.__label_send_message = Label(self.__root, text='Send Message')
        self.__label_topic = Label(self.__root, text='Topic')

        """ Create the gui entries """
        self.__entry_username = Entry(self.__root)
        self.__entry_password = Entry(self.__root, show='*')
        self.__entry_topic = Entry(self.__root)
        self.__entry_message_send = Entry(self.__root)

        """ Create the gui buttons """
        self.__button_quit = Button(self.__root, text="Quit", command=self.__root.quit)
        self.__button_send = Button(self.__root, text="Send", command=self.__send_callback)
        self.__button_connect = Button(self.__root, text="Connect", width=10, command=self.__connect_button_callback)

        """ Create the gui text box """
        self.__text_box_receive = Text(self.__root, width=50, height=10)
        self.__text_box_send = Text(self.__root, width=50, height=10)

        """ Create the connect interface """
        self.create_connect_gui()

    def __send_callback(self):
        self.__client.publish()

    """ The connect callback function """
    def __connect_button_callback(self):
        self.__client = Client("123", username=self.__entry_username.get(), password=self.__entry_password.get())  # Create a client object when the connect button is pressed
        self.__client.connect()

        if self.__client.get_is_connected() is True:
            """If we successfully connect to the broker
            we dispose the tkinter objects in the root and create the next state"""
            self.dispose_connect_gui()
            self.create_main_gui()

    """ This method starts the tkinter event loop """
    def run(self):
        self.__root.mainloop()

    """ This method creates the connect interface """
    def create_connect_gui(self):
        def motion(event):  # A motion callback function
            print(event.x, event.y)

        """ Place all the widgets on the frame to create the connect interface """
        # Buttons
        self.__button_quit.place(bordermode=OUTSIDE, x=self.__width / 10 * 9, y=self.__height / 10 * 9)
        self.__root.bind("<Button-1>", motion)  # Bind the motion function to be called whenever the left click is pressed
        self.__button_connect.place(x=self.__width / 3 + 100, y=self.__height / 5 + 100)

        # Labels
        self.__label_username.place(x=self.__width / 3, y=self.__height / 5)
        self.__label_password.place(x=self.__width / 3, y=self.__height / 5 + 30)

        # Entries
        self.__entry_username.focus_set()
        self.__entry_username.place(x=self.__width / 3 + 90, y=self.__height / 5)
        self.__entry_password.place(x=self.__width / 3 + 90, y=self.__height / 5 + 30)

    """ This method deletes the position of the widgets from the connect interface
        but it doesn't destroy the widgets so we can use them later if needed """
    def dispose_connect_gui(self):
        # Labels
        self.__label_username.place_forget()
        self.__label_password.place_forget()

        # Entries
        self.__entry_password.place_forget()
        self.__entry_username.place_forget()

        # Buttons
        self.__button_connect.place_forget()

        self.__root.update()

    """ Create_main_gui method places all the widgets necessary for the main interface """
    def create_main_gui(self):
        # Entries
        self.__entry_topic.place(x=self.__width/8, y=self.__height/7)
        self.__entry_message_send.place(x=self.__width/8, y=self.__height/7+30)

        # Buttons
        self.__button_send.place(bordermode=OUTSIDE, x=self.__width/8+45, y=self.__height/7+60)

        # Labels
        self.__label_topic.place(x=self.__width/8-60, y=self.__height/7)
        self.__label_send_message.place(x=self.__width/8-110, y=self.__height/7+30)

        # Text boxes
        self.__text_box_receive.place(x=self.__width/5*2, y=self.__height/7)

    """ This method deletes the position of the widgets from the main interface
        but it doesn't destroy the widgets so we can use them later if needed """
    def dispose_main_gui(self):
        # Entries
        self.__entry_topic.place_forget()
        self.__entry_message_send.forget()

        # Buttons
        self.__button_send.place_forget()

        # Labels
        self.__label_topic.place_forget()

        # Text boxes
        self.__text_box_receive.place_forget()
        self.__text_box_send.place_forget()
