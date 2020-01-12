import socket
import traceback

""" Create an Connection class to handle the packets transfer on the socket. """
class Connection:

    def __init__(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__socket.settimeout(30)
        self.__host_ip = socket.gethostbyname('mqtt.eclipse.org')

    def establish_connection(self):
        print("ip:", self.__host_ip)
        try:
            self.__socket.connect((self.__host_ip, 1883))
        except socket.error:
            traceback.print_exc()

    def set_host_ip(self, _ip):
        self.__host_ip = _ip

    """Send a packets(byte array) with the socket created"""
    def send(self, packet):
        self.__socket.sendall(packet)

    """Receive a packets(byte array) with the socket created"""
    def receive(self, byte_size):
        return self.__socket.recv(byte_size)
