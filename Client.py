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

    def __init__(self, client_id, topic=None, username=None, password=None):
        self.__username = username
        self.__client_id = client_id
        self.__password = password
        self.__topic = topic
        self.__connection = conn.Connection()
        self.__thread = None
        self.__is_connected = False
        self.__packet_fields = {
            'protocol_name': "MQTT",
            'keep_alive': b'\x00\x05',  # keep alive
            'properties': b'\x11\x00\x00\x00\x0a',  # properties
            'connect_flags': b'\x02',  # connect flags
            'version': b'\5'
        }

    """ Defining the connect action. """
    def connect(self):
        connect_packet = Connect()
        connect_packet.set_username(self.__username)
        connect_packet.set_password(self.__password)

        packet = connect_packet.parse()

        self.__connection.send(packet)  # Send the connect packet
        received_packet = self.__connection.receive(1024)  # Receive the response packet
        print(repr(received_packet))
        """The received packet is an acknowledgement packet 
        and the bytes received do not contain the header identifier of the packet"""
        if received_packet[3:4] == b'\x00':  # Verify the reason code; it is the 3rd byte: 0-> success
            print("Connection acknowledged")
            self.__is_connected = True
        else:
            print("Connection dropped")

    def disconnect(self):
        disconnect_packet = Disconnect()

    def publish(self):
        publish_packet = Publish()

    def subscribe(self):
        subscribe_packet = Subscribe()

    def unsubscribe(self):
        unsubscribe_packet = Unsubscribe()

    def get_is_connected(self):
        return self.__is_connected
