import socket
import traceback


class Connection(object):

    def __init__(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__socket.settimeout(30)
        host_ip = socket.gethostbyname('mqtt.eclipse.org')
        print("ip:", host_ip)
        try:
            self.__socket.connect((host_ip, 1883))
        except socket.error:
            traceback.print_exc()
    """Send a packet (bytearray ) with the socket created"""
    def send(self, packet):
        self.__socket.sendall(packet)

    """Receive a packet(bytearray) with the socket created"""
    def receive(self, byte_size):
        return self.__socket.recv(byte_size)
