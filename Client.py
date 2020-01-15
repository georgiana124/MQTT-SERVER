"""
default host
broker test host
mqtt.eclipse.org
port 1883
"""
import Connection as conn
from collections import namedtuple
from mqtt_packets import *
packet_struct = namedtuple('packet_struct', ['message', 'byte_packet'])


""" The Client class defines the behaviour of the user. """
class Client:

    def __init__(self, client_id, username=None, password=None, host_ip=None):
        self.__username = username
        self.__client_id = client_id
        self.__password = password
        self.__host_ip = host_ip
        self.__topics = []
        self.__connection = conn.Connection()
        self.__thread = None
        self.__is_connected = False
        self.__packet_struct = packet_struct(message='', byte_packet=bytearray())

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
        self.__packet_struct.byte_packet = self.__connection.receive(1024)  # Receive the response packet
        print(repr(self.__packet_struct.byte_packet))
        """The received packet is an acknowledgement packet 
        and the bytes received do not contain the header identifier of the packet"""
        if self.__packet_struct.byte_packet[3:4] == b'\x00':  # Verify the reason code; it is the 3rd byte: 0-> success
            self.__is_connected = True
            self.__packet_struct.message = "Connect: success.\n"
            return self.__packet_struct
        else:
            self.__packet_struct.message = "Connect: failed.\n"
            return self.__packet_struct

    """ Defining the disconnect action. """
    def disconnect(self):
        disconnect_packet = Disconnect()
        packet = disconnect_packet.parse()
        self.__connection.send(packet)
        self.__packet_struct.byte_packet = self.__connection.receive(1024)
        if self.__packet_struct.byte_packet[0:1] == b'\x00':
            self.__is_connected = False
            self.__packet_struct.message = "Disconnect: success.\n"
            return self.__packet_struct
        else:
            self.__packet_struct.message = "Disconnect: failed.\n"
            return self.__packet_struct

    """ Defining the publish action. """
    def publish(self):
        publish_packet = Publish()
        packet = publish_packet.parse()
        self.__connection.send(packet)
        self.__packet_struct.byte_packet = self.__connection.receive(1024)
        if self.__packet_struct.byte_packet[0:1] == b'':
            self.__packet_struct.message = "Publish: success.\n"
            return self.__packet_struct
        else:
            self.__packet_struct.message = "Publish: failed.\n"
            return self.__packet_struct

    """ Defining the subscribe action. """
    def subscribe(self):
        subscribe_packet = Subscribe()
        subscribe_packet.set_topics(self.__topics)
        packet = subscribe_packet.parse()
        self.__connection.send(packet)
        self.__packet_struct.byte_packet = self.__connection.receive(1024)
        if self.__packet_struct.byte_packet[0:1] == b'':
            self.__packet_struct.message = "Subscribe: success.\n"
            return self.__packet_struct
        else:
            self.__packet_struct.message = "Subscribe: failed.\n"
            return self.__packet_struct

    """ Defining the unsubscribe action. """
    def unsubscribe(self):
        unsubscribe_packet = Unsubscribe()
        packet = unsubscribe_packet.parse()
        self.__connection.send(packet)
        self.__packet_struct.byte_packet = self.__connection.receive(1024)
        if self.__packet_struct.byte_packet[0:1] == b'':
            self.__packet_struct.message = "Unsubscribe: success.\n"
            return self.__packet_struct
        else:
            self.__packet_struct.message = "Unsubscribe failed.\n"
            return self.__packet_struct

    """ Getter method for is_connected field. """
    def get_is_connected(self):
        return self.__is_connected

    """ Append method for the list of topics. """
    def add_topic(self, _topic):
        self.__topics.append(_topic)
