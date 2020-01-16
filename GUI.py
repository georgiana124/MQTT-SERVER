from tkinter import *
from tkinter.ttk import Combobox
from Client import *
import binascii
from my_threads import *

""" The GUI class handles the front end of the app: what does the user see.
    It uses tkinter and contains all the graphical elements. """
class GUI:

    def __init__(self):
        self.__client = None
        self.__root = Tk()  # Create the main root for the app
        self.__width = 1400
        self.__height = 800
        self.__text_box_log_col = 0
        self.__gui_thread = None
        self.__ping_thread = None
        self.__send_thread = None

        """ Create a root app based on the width and height defined """
        self.__root.geometry(str(self.__width) + "x" + str(self.__height))
        self.__root.title("MQTT Client")
        self.__root.configure(background='PeachPuff2')

        """ Create the gui labels """
        self.__label_username = Label(self.__root, text='Username')
        self.__label_password = Label(self.__root, text='Password')
        self.__label_receive_message = Label(self.__root, text='Received message')
        self.__label_send_message = Label(self.__root, text='Sent Message')
        self.__label_publish_message = Label(self.__root, text='Message')
        self.__label_topic = Label(self.__root, text='Topic')
        self.__label_subscribe_to = Label(self.__root, text='Subscribe to')
        self.__label_qos = Label(self.__root, text='QoS')
        self.__label_logger = Label(self.__root, text='Logger')

        """ Create the gui entries """
        self.__entry_username = Entry(self.__root)
        self.__entry_password = Entry(self.__root, show='*')
        self.__entry_topic = Entry(self.__root)
        self.__entry_message_send = Entry(self.__root)
        self.__entry_subscribe = Entry(self.__root)

        """ Create the gui buttons """
        self.__button_quit = Button(self.__root, text="Quit", command=self.__root.quit)
        self.__button_send = Button(self.__root, text="Send", command=self.__send_button_callback)
        self.__button_disconnect = Button(self.__root, text="Disconnect", command=self.__disconnect_button_callback)
        self.__button_connect = Button(self.__root, text="Connect", width=10, command=self.__connect_button_callback)
        self.__button_subscribe = Button(self.__root, text="Subscribe", width=10, command=self.__subscribe_button_callback)
        self.__button_unsubscribe = Button(self.__root, text="Unsubscribe", width=10, command=self.__unsubscribe_button_callback)

        """ Create the gui text box """
        self.__text_box_receive = Text(self.__root, width=50, height=10)
        self.__text_box_send = Text(self.__root, width=50, height=10)
        self.__text_box_log = Text(self.__root, width=50, height=30, bg='black', fg='SpringGreen2')

        """ Create qos combo box. """
        self.__qos_combo_box = Combobox(self.__root, values=['0', '1', '2'], width=5)
        self.__qos_combo_box.current(0)

        """ Create the connect interface """
        self.create_connect_gui()

    def __text_box_log_increase(self):
        self.__text_box_log_col += 1  # Increase column numbers in log box

    """ Keep only the last 5 actions in the log. """
    def __text_box_log_clear(self):
        if self.__text_box_log_col == 5:
            self.__text_box_log.delete('1.0', END)
            self.__text_box_log_col = 0

    """ Add a new entry to the log. """
    def __text_box_log_update(self, _packet_struct):
        """Updating the log"""
        self.__text_box_log_clear()
        self.__text_box_log.insert(END, _packet_struct.message + "\nPacket:" + repr(binascii.hexlify(_packet_struct.byte_code)) + "\n\n")
        self.__text_box_log_increase()

    """ This method starts the tkinter event loop. """
    def run(self):
        self.__gui_thread = Thread(target=self.__root.mainloop())
        self.__gui_thread.start()

    """ Unsubscribe button callback method. """
    def __unsubscribe_button_callback(self):
        self.__send_thread = Thread(target=self.__client.unsubscribe)
        self.__send_thread.run()
        struct_received = result.get()
        self.__text_box_log_update(struct_received)

    """ Send button callback method. """
    def __send_button_callback(self):
        self.__text_box_receive.config(state=NORMAL)
        self.__text_box_receive.delete('1.0', END)  # Delete text box content before showing new published content
        self.__send_thread = Thread(target=self.__client.publish)
        self.__send_thread.run()
        struct_received = result.get()  # Get the response from the server
        self.__text_box_receive.insert(INSERT, "ASC")
        self.__text_box_receive.config(state=DISABLED)

        self.__text_box_log_update(struct_received)

    """ Subscribe button callback method. """
    def __subscribe_button_callback(self):
        topic_subscribe = self.__entry_subscribe.get()
        self.__client.add_topic(topic_subscribe)
        self.__text_box_send.config(state=NORMAL)
        self.__text_box_send.delete('1.0', END)  # Delete text box content before showing new received content
        self.__send_thread = Thread(target=self.__client.subscribe)
        self.__send_thread.run()
        struct_received = result.get()  # Get the response from the server
        self.__text_box_send.config(state=DISABLED)

        self.__text_box_log_update(struct_received)

    """ The connect callback function """
    def __connect_button_callback(self):
        self.__client = Client("123", username=self.__entry_username.get(), password=self.__entry_password.get(), qos=int(self.__qos_combo_box.get()))  # Create a client object when the connect button is pressed

        self.__send_thread = Thread(target=self.__client.connect)
        self.__send_thread.run()

        struct_received = result.get()  # Get the response from the server

        self.__text_box_log_update(struct_received)

        if self.__client.get_is_connected() is True:
            """ If we successfully connect to the broker
            we dispose the tkinter objects in the root and create the next state """
            self.dispose_connect_gui()
            self.create_main_gui()
            self.__ping_thread = Ping_Thread(5, self.__client.pingreq)

    """ Disconnect button callback method. """
    def __disconnect_button_callback(self):
        self.__send_thread = Thread(target=self.__client.disconnect)
        self.__send_thread.run()
        struct = packet_struct()
        struct.message = "Disconnect: success"

        struct.byte_code = b''
        self.__text_box_log_update(struct)
        if self.__client.get_is_connected() is False:
            """ If we successfully disconnect from the broker
            we go back to the connect page"""
            self.dispose_main_gui()
            self.__ping_thread.stop()  # Stop the ping request packet sender
            self.create_connect_gui()

    """ This method creates the connect interface. """
    def create_connect_gui(self):
        """ Place all the widgets on the frame to create the connect interface. """
        # Buttons
        self.__button_quit.place(bordermode=OUTSIDE, x=self.__width / 10 * 9, y=self.__height / 10 * 9)
        self.__button_connect.place(x=self.__width / 3 + 100, y=self.__height / 5 + 100)

        # Labels
        self.__label_username.place(x=self.__width / 3, y=self.__height / 5)
        self.__label_password.place(x=self.__width / 3, y=self.__height / 5 + 30)
        self.__label_qos.place(x=self.__width/3+270, y=self.__height/5)
        self.__label_logger.place(x=self.__width/5*3.5, y=self.__height/7-30)

        # Entries
        self.__entry_username.focus_set()
        self.__entry_username.place(x=self.__width / 3 + 90, y=self.__height / 5)
        self.__entry_password.place(x=self.__width / 3 + 90, y=self.__height / 5 + 30)

        # Text box
        self.__text_box_log.place(x=self.__width/5*3.5, y=self.__height/7)

        # Combo box
        self.__qos_combo_box.place(x=self.__width / 3 + 300, y=self.__height / 5)

        self.__root.update()

    """ This method deletes the position of the widgets from the connect interface
    but it doesn't destroy the widgets so we can use them later if needed. """
    def dispose_connect_gui(self):
        # Labels
        self.__label_username.place_forget()
        self.__label_password.place_forget()
        self.__label_qos.place_forget()

        # Entries
        self.__entry_password.place_forget()
        self.__entry_username.place_forget()

        # Buttons
        self.__button_connect.place_forget()

        # Combo box
        self.__qos_combo_box.place_forget()

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
        self.__button_unsubscribe.place(bordermode=OUTSIDE, x=self.__width/8+30, y=self.__height*3/7+60)

        # Labels
        self.__label_topic.place(x=self.__width/8-60, y=self.__height/7)
        self.__label_send_message.place(x=self.__width/8-110, y=self.__height/7+30)
        self.__label_subscribe_to.place(x=self.__width/8-100, y=self.__height*3/7)
        self.__label_send_message.place(x=self.__width/5*2, y=self.__height/7*3-30)
        self.__label_receive_message.place(x=self.__width/5*2, y=self.__height/7-30)
        self.__label_publish_message.place(x=self.__width/8-60, y=self.__height/7+30)

        # Text boxes
        self.__text_box_receive.place(x=self.__width/5*2, y=self.__height/7)
        self.__text_box_send.place(x=self.__width/5*2, y=self.__height/7*3)

        self.__root.update()

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
        self.__button_unsubscribe.place_forget()

        # Labels
        self.__label_topic.place_forget()
        self.__label_subscribe_to.place_forget()
        self.__label_send_message.place_forget()
        self.__label_receive_message.place_forget()
        self.__label_publish_message.place_forget()

        # Text boxes
        self.__text_box_receive.delete('1.0', END)
        self.__text_box_send.delete('1.0', END)
        self.__text_box_receive.place_forget()
        self.__text_box_send.place_forget()

        self.__root.update()
