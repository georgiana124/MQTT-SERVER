"""
default host
broker test host
mqtt.eclipse.org
port 1883
"""
import Connection as conn


class Client(object):

    def __init__(self, client_id, topic=None, username=None, password=None, keep_alive=60, message_retry=20):
        self.__username = username
        self.__client_id = client_id
        self.__password = password
        self.__topic = topic
        self.__connection = conn.Connection()
        self.__socket = None
        self.__thread = None

    def connect(self):
        packet = bytearray(b'\x10\x0b\x04')
        protocol_name = "MQTT"  # 04MQTT
        packet.extend(protocol_name.encode('UTF-8'))

        """
            connect_flags bits
        username flag=1
        password flag =1
        will retain = 0
        will qos=01
        will flag=1
        clean start=1
        reserved =0
        """
        packet.extend(b'\x05\x02\x05\x03')
        packet.extend(self.__client_id.encode('UTF-8'))
        #packet.extend(self.__username.encode('UTF-8'))
        #packet.extend(self.__password.encode('UTF-8'))

        self.__connection.send(packet)

    def publish(self, dup=False, qos=0x01, retain=False):
        pass

    def subscribe(self):
        pass
