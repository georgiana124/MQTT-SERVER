"""
default host
broker test host
mqtt.eclipse.org
port 1883

CONNECT = 0x10
CONNACK = 0x20
PUBLISH = 0x30
PUBACK = 0x40
PUBREC = 0x50
PUBREL = 0x62
PUBCOMP = 0x70
SUBSCRIBE = 0x82
SUBACK = 0x90
UNSUBSCRIBE = 0xA2
UNSUBACK = 0xB0
PINGREQ = 0xC0
PINGRESP = 0xD0
DISCONNECT = 0xE0
AUTH = 0xF0
"""
import Connection as conn
CONNECT = b'\x10'


class Client(object):

    def __init__(self, client_id, topic=None, username=None, password=None):
        self.__username = username
        self.__client_id = client_id
        self.__password = password
        self.__topic = topic
        self.__connection = conn.Connection()
        self.__socket = None
        self.__thread = None
        self.__protocol_name = "MQTT"
        self.__is_connected = False

    def connect(self):
        packet = bytearray()  # initialize the packet to be sent
        connect_flags = b'\x02'  # connect flags
        keep_alive = b'\x00\x05'  # keep alive
        properties = b'\x11\x00\x00\x00\x0a'  # properties
        variable_header = bytearray()  # initialize an empty byte array to create the variable header
        packet += CONNECT
        variable_header += b'\x00'
        variable_header += bytes([len(self.__protocol_name)])
        variable_header += self.__protocol_name.encode('UTF-8')
        variable_header += b'\5'  # version 5
        variable_header += connect_flags
        variable_header += keep_alive
        variable_header += bytes([len(properties)])
        variable_header += properties
        variable_header += b'\x00'
        variable_header += bytes([len(self.__username)])
        variable_header += self.__username.encode('UTF-8')

        packet_length = bytes([len(variable_header)])  # calculate the length of the remaining packet
        packet += packet_length  # add the length as bytes to the packet
        packet += variable_header  # add the whole variable_header to the packet

        # Send the connect packet
        self.__connection.send(packet)
        # Receive the response packet
        received_packet = self.__connection.receive(1024)
        # The received packet is an acknowledgement packet and the bytes received do not contain the header indentifier of the packet
        if received_packet[3:4] == b'\x00':  # Verify the reason code; it is the 3rd byte: 0-> success
            print("Connection acknowledged")
            self.__is_connected = True
        else:
            print("Connection dropped")

    def publish(self, dup=False, qos=0x01, retain=False):
        pass

    def subscribe(self):
        pass

    def get_is_connected(self):
        return self.__is_connected
