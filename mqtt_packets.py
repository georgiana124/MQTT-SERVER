from abc import ABC, abstractmethod


""" Define the Packet abstract class, the super class of each packet type to be defined.
    Connect packet actions:
    -> if the server doesn't receive a CONNECT packet within a reasonable amount of time 
    after the Network Connection is established, the Server SHOULD close the Network Connection
    -> """
class Packet(ABC):

    def __init__(self):

        self.packet_fixed_header = {
            'CONNECT': b'\x10',
            'CONNACK': b'\x20',
            'PUBLISH': b'\x30',
            'PUBACK': b'\x40',
            'PUBREC': b'\x50',
            'PUBREL': b'\x62',
            'PUBCOMP': b'\x70',
            'SUBSCRIBE': b'\x82',
            'SUBACK': b'\x90',
            'UNSUBSCRIBE': b'\xA2',
            'UNSUBACK': b'\xB0',
            'PINGREQ': b'\xC0',
            'PINGRESP': b'\xD0',
            'DISCONNECT': b'\xE0',
            'AUTH': b'\xF0',
        }

    @abstractmethod
    def parse(self):
        pass


""" Implement the Connect Class. This class inherits the abc Packet and implements an parsing method which creates a connect packet based on some options. """
class Connect(Packet):

    qos = 0

    packet_payload = {
        'client_id': bytearray(),  """ identifies the client to the server; it must be present; must be encoded string UTF-8"""
        'will_topic': bytearray(),  """ if the will flag is set will properties is the next field in payload """
        'will_topic': bytearray(),
        'will_payload': bytearray(),
        'username': "",
        'password': ""
    }
    packet_variable_header = {
        'protocol_name': "MQTT",
        'version': b'\x05',
        'connect_flags': b'\x02',  # connect flags
        'keep_alive': b'\x00\x05',  # keep alive
        'properties': b'\x11\x00\x00\x00\x0a',  # properties
    }

    def set_qos(self, _qos):
        self.qos = _qos

    def set_username(self, _username):
        self.packet_payload['username'] = _username

    def set_password(self, _password):
        self.packet_payload['password'] = _password

    def parse(self):
        packet = bytearray()  # initialize the packet to be sent
        variable_header = bytearray()  # initialize an empty byte array to create the variable header

        # Add fixed header
        packet += self.packet_fixed_header['CONNECT']

        # Variable header
        variable_header += b'\x00'  # Add a offset to the length field
        variable_header += bytes([len(self.packet_variable_header['protocol_name'])])
        variable_header += self.packet_variable_header['protocol_name'].encode('UTF-8')
        variable_header += self.packet_variable_header['version']  # version 5
        variable_header += self.packet_variable_header['connect_flags']
        variable_header += self.packet_variable_header['keep_alive']
        variable_header += bytes([len(self.packet_variable_header['properties'])])
        variable_header += self.packet_variable_header['properties']

        # Payload
        payload = b'\x00'
        payload += bytes([len(self.packet_payload['username'])])
        payload += self.packet_payload['username'].encode('UTF-8')
        variable_header += payload

        # Arrange the final packet
        packet_length = bytes([len(variable_header)])  # calculate the length of the remaining packet
        packet += packet_length  # add the length as bytes to the packet
        packet += variable_header  # add the whole variable_header to the packet
        return packet


class Disconnect(Packet):

    variable_header = {
        'reason_code': b'\x00',
        'properties': b'\x05\x11\x00\x00\x00\x00'  
        """ length(variable byte integer) =5(x05)->expiry interval = 17(x11)-> 
            session expiry interval = 0(x00x00x00x00)"""
    }

    def parse(self):
        packet = bytearray()
        packet += self.packet_fixed_header['DISCONNECT']

        variable_header = self.variable_header['reason_code']
        variable_header += self.variable_header['properties']

        remaining_legth = bytes([len(variable_header)])

        packet += remaining_legth
        packet += variable_header

        return packet

class Publish(Packet):

    variable_header = {
        'topic_name': bytearray(),  # string utf8 encoded
        'packet_identifier': '\x00\x0a',
        'properties': b'\x00'  # no properties
    }

    def parse(self):
        packet = bytearray()
        return packet

class Subscribe(Packet):

    """ Contains only the field packet identifier and properties. """
    variable_header = {
        'packet_identifier': b'',
        'properties': b''
    }

    """ The payload contains a list of topic filters indicating the topics to which
        the client wants to subscribe. """
    payload = {

    }

    def parse(self):
        packet = bytearray()
        variable_header = bytearray()
        payload = bytearray()

        packet += self.packet_fixed_header['SUBSCRIBE']
        remain_length = bytes()

        return packet

class Unsubscribe(Packet):

    def parse(self):
        packet = bytearray()
        return packet
