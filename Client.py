"""
default host
broker test host
mqtt.eclipse.org
port 1883
"""
import Connection as conn
from packet_struct import *
from mqtt_packets import *


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
        self.__struct = packet_struct()

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
        self.__struct.byte_code = self.__connection.receive(1024)  # Receive the response packet
        print(repr(self.__struct.byte_code))
        """The received packet is an acknowledgement packet 
        and the bytes received do not contain the header identifier of the packet"""
        if self.__struct.byte_code[3:4] == b'\x00':  # Verify the reason code; it is the 3rd byte: 0-> success
            self.__is_connected = True
            self.__struct.message = "Connect: success."
            return self.__struct
        else:
            self.__struct.message = "Connect: failed."
            return self.__struct

    """ Defining the disconnect action. """
    def disconnect(self):
        disconnect_packet = Disconnect()
        packet = disconnect_packet.parse()
        self.__connection.send(packet)
        self.__struct.byte_code = self.__connection.receive(1024)
        if self.__struct.byte_code[0:1] == b'\x00':
            self.__is_connected = False
            self.__struct.message = "Disconnect: success."
            return self.__struct
        else:
            self.__struct.message = "Disconnect: failed."
            return self.__struct

    """ Defining the publish action. """
    def publish(self):
        publish_packet = Publish()
        packet = publish_packet.parse()
        self.__connection.send(packet)
        self.__struct.byte_code = self.__connection.receive(1024)
        if self.__struct.byte_code[0:1] == b'':
            self.__struct.message = "Publish: success."
            return self.__struct
        else:
            self.__struct.message = "Publish: failed."
            return self.__struct

    """ Defining the subscribe action. """
    def subscribe(self):
        subscribe_packet = Subscribe()
        subscribe_packet.set_topics(self.__topics)
        packet = subscribe_packet.parse()
        self.__connection.send(packet)
        packet_received = self.__connection.receive(1024)
        self.__struct.byte_code = packet_received
        if self.__struct.byte_code[-1:] == b'\x01' or self.__struct.byte_code[-1:] == b'\x02' or self.__struct.byte_code[-1:] == b'\x00':
            self.__struct.message = "Subscribe: success.\n"
            return self.__struct
        else:
            self.__struct.message = "Subscribe: failed.\n"
            return self.__struct

    """ Defining the unsubscribe action. """
    def unsubscribe(self):
        unsubscribe_packet = Unsubscribe()
        packet = unsubscribe_packet.parse()
        self.__connection.send(packet)
        self.__struct.byte_code = self.__connection.receive(1024)
        if self.__struct.byte_code[0:1] == b'':
            self.__struct.message = "Unsubscribe: success.\n"
            return self.__struct
        else:
            self.__struct.message = "Unsubscribe failed.\n"
            return self.__struct

    """ Getter method for is_connected field. """
    def get_is_connected(self):
        return self.__is_connected

    """ Append method for the list of topics. """
    def add_topic(self, _topic):
        self.__topics.append(_topic)
