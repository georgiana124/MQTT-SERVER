import socket
import traceback


class Connection(object):

    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.settimeout(30)
        host_ip = socket.gethostbyname('mqtt.eclipse.org')
        print("ip:", host_ip)
        try:
            self._socket.connect((host_ip, 1883))
        except socket.error:
            traceback.print_exc()

    def send(self, packet):
        self._socket.send(packet.encode("UTF-8"))