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
        self.__root.configure(background='#40E0D0')

        """ Create the gui labels """
        self.__label_username = Label(self.__root, text='Username')
        self.__label_password = Label(self.__root, text='Password')
        self.__label_receive_message = Label(self.__root, text='Received message')
        self.__label_send_message = Label(self.__root, text='Send Message')
        self.__label_topic = Label(self.__root, text='Topic')
        self.__label_subscribe_to = Label(self.__root, text='Subscribe to')

        """ Create the gui entries """
        self.__entry_username = Entry(self.__root)
        self.__entry_password = Entry(self.__root, show='*')
        self.__entry_topic = Entry(self.__root)
        self.__entry_message_send = Entry(self.__root)
        self.__entry_subscribe = Entry(self.__root)

        """ Create the gui buttons """
        self.__button_quit = Button(self.__root, text="Quit", command=self.__root.quit)
        self.__button_send = Button(self.__root, text="Send", command=self.__send_callback)
        self.__button_disconnect = Button(self.__root, text="Disconnect", command=self.__disconnect_callback)
        self.__button_connect = Button(self.__root, text="Connect", width=10, command=self.__connect_button_callback)
        self.__button_subscribe = Button(self.__root, text="Subscribe", width=10, command=self.__subscribe_button_callback)

        """ Create the gui text box """
        self.__text_box_receive = Text(self.__root, width=50, height=10)
        self.__text_box_send = Text(self.__root, width=50, height=10)
        self.__text_box_receive_subscribed = Text(self.__root, width=50, height=10)
        """ Create the connect interface """
        self.create_connect_gui()

    def __send_callback(self):
        self.__text_box_receive.config(state=NORMAL)
        self.__text_box_receive.delete('1.0', END) #Delete text box content before showing new published content
        #self.__client.publish()
        self.__text_box_receive.insert(INSERT, "ASC")
        self.__text_box_receive.config(state=DISABLED)

    def __subscribe_button_callback(self):
        topic_subscribe = self.__entry_subscribe.get()
        self.__client.add_topic(topic_subscribe)
        self.__text_box_receive_subscribed.config(state=NORMAL)
        self.__text_box_receive_subscribed.delete('1.0', END)  # Delete text box content before showing new received content
        self.__client.subscribe()
        self.__text_box_receive_subscribed.config(state=DISABLED)

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

    def __disconnect_callback(self):
        self.__client.disconnect()

        if self.__client.get_is_connected() is False:
            """ If we successfully disconnect from the broker
            we go back to the connect page"""
            self.dispose_main_gui()
            self.create_connect_gui()

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
        self.__entry_subscribe.place(x=self.__width/8, y=self.__height*3/7)

        # Buttons
        self.__button_send.place(bordermode=OUTSIDE, x=self.__width/8+45, y=self.__height/7+60)
        self.__button_subscribe.place(border=OUTSIDE, x=self.__width/8+30, y=self.__height*3/7+30)
        self.__button_disconnect.place(bordermode=OUTSIDE, x=self.__width / 10 * 9, y=self.__height / 10 * 8.5)

        # Labels
        self.__label_topic.place(x=self.__width/8-60, y=self.__height/7)
        self.__label_send_message.place(x=self.__width/8-110, y=self.__height/7+30)
        self.__label_subscribe_to.place(x=self.__width/8-100, y=self.__height*3/7)

        # Text boxes
        self.__text_box_receive.place(x=self.__width/5*2, y=self.__height/7)
        self.__text_box_receive_subscribed.place(x=self.__width/5*2,y=self.__height/7*3)


    """ This method deletes the position of the widgets from the main interface
        but it doesn't destroy the widgets so we can use them later if needed """
    def dispose_main_gui(self):
        # Entries
        self.__entry_topic.place_forget()
        self.__entry_message_send.place_forget()
        self.__entry_subscribe.place_forget()

        # Buttons
        self.__button_send.place_forget()
        self.__button_subscribe.place_forget()
        self.__button_disconnect.place_forget()

        # Labels
        self.__label_topic.place_forget()
        self.__label_subscribe_to.place_forget()
        self.__label_send_message.place_forget()

        # Text boxes
        self.__text_box_receive.place_forget()
        self.__text_box_send.place_forget()
        self.__text_box_receive_subscribed.place_forget()

        self.__root.update()
