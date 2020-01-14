"""
default host
broker test host
mqtt.eclipse.org
port 1883
"""
import Connection as conn
from mqtt_packets import *

""" The Client class defines the behaviour of the user. """
class Client:

    def __init__(self, client_id, topic=None, username=None, password=None, host_ip=None):
        self.__username = username
        self.__client_id = client_id
        self.__password = password
        self.__host_ip = host_ip
        self.__topics = []
        self.__connection = conn.Connection()
        self.__thread = None
        self.__is_connected = False

    """ Defining the connect action. """
    def connect(self):
        self.__connection.establish_connection()
        if self.__host_ip is not None:
            self.__connection.set_host_ip(self.__host_ip)

        connect_packet = Connect()
        connect_packet.set_username(self.__username)
        connect_packet.set_password(self.__password)

        packet = connect_packet.parse()

        self.__connection.send(packet)  # Send the connect packet
        received_packet = self.__connection.receive(2048)  # Receive the response packet
        print(repr(received_packet))
        """The received packet is an acknowledgement packet 
        and the bytes received do not contain the header identifier of the packet"""
        if received_packet[3:4] == b'\x00':  # Verify the reason code; it is the 3rd byte: 0-> success
            print("Connection acknowledged")
            self.__is_connected = True
        else:
            print("Connection dropped")

    """ Defining the disconnect action. """
    def disconnect(self):
        disconnect_packet = Disconnect()
        packet = disconnect_packet.parse()

        self.__connection.send(packet)
        self.__is_connected = False

    """ Defining the publish action. """
    def publish(self):
        publish_packet = Publish()
        packet = publish_packet.parse()

        self.__connection.send(packet)

    """ Defining the subscribe action. """
    def subscribe(self):
        subscribe_packet = Subscribe()
        packet = subscribe_packet.parse()

        self.__connection.send(packet)

    """ Defining the unsubscribe action. """
    def unsubscribe(self):
        unsubscribe_packet = Unsubscribe()
        packet = unsubscribe_packet.parse()

        self.__connection.send(packet)

    def get_is_connected(self):
        return self.__is_connected

    def add_topic(self, _topic):
        self.__topics.append(_topic)
