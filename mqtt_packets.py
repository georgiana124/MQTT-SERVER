from abc import ABC, abstractmethod


""" Define the Packet abstract class, the super class of each packet type to be defined. """
class Packet(ABC):

    def __init__(self):
        self.packet_fields = {
            'protocol_name': "MQTT",
            'keep_alive': b'\x00\x05',  # keep alive
            'properties': b'\x11\x00\x00\x00\x0a',  # properties
            'connect_flags': b'\x02',  # connect flags
            'version': b'\5'
        }
        self.packet_fixed_header = {
            'connect': b'\x10',
            'connack': b'\x20',
            'publish': b'\x30',
            'puback': b'\x40',
            'pubrec': b'\x50',
            'pubrel': b'\x62',
            'pubcomp': b'\x70',
            'subscribe': b'\x82',
            'suback': b'\x90',
            'unsubscribe': b'\xA2',
            'unsuback': b'\xB0',
            'pingreq': b'\xC0',
            'pingresp': b'\xD0',
            'disconnect': b'\xE0',
            'auth': b'\xF0',
        }

    @abstractmethod
    def parse(self):
        pass


""" Implement the Connect Class. This class inherits the abc Packet and implements an parsing method which creates a connect packet based on some options. """
class Connect(Packet):

    username = ""
    password = ""
    qos = 1

    def set_qos(self, _qos):
        self.qos = _qos

    def set_username(self, _username):
        self.username = _username

    def set_password(self, _password):
        self.password = _password

    def parse(self):
        packet = bytearray()  # initialize the packet to be sent
        variable_header = bytearray()  # initialize an empty byte array to create the variable header

        # Add fixed header
        packet += self.packet_fixed_header['connect']

        # Variable header
        variable_header += b'\x00'
        variable_header += bytes([len(self.packet_fields['protocol_name'])])
        variable_header += self.packet_fields['protocol_name'].encode('UTF-8')
        variable_header += self.packet_fields['version']  # version 5
        variable_header += self.packet_fields['connect_flags']
        variable_header += self.packet_fields['keep_alive']
        variable_header += bytes([len(self.packet_fields['properties'])])
        variable_header += self.packet_fields['properties']
        variable_header += b'\x00'

        # Payload
        payload = bytes([len(self.username)])
        payload += self.username.encode('UTF-8')
        variable_header += payload

        # Arrange the final packet
        packet_length = bytes([len(variable_header)])  # calculate the length of the remaining packet
        packet += packet_length  # add the length as bytes to the packet
        packet += variable_header  # add the whole variable_header to the packet
        return packet


class Disconnect(Packet):

    def parse(self):
        packet = bytearray()
        return packet

class Publish(Packet):

    def parse(self):
        packet = bytearray()
        return packet

class Subscribe(Packet):

    def parse(self):
        packet = bytearray()
        return packet

class Unsubscribe(Packet):

    def parse(self):
        packet = bytearray()
        return packet
