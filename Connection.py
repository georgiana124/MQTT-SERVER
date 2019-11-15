import socket
import traceback


class Connection(object):

    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.settimeout(30)
        host_ip = socket.gethostbyname('mqtt.eclipse.org')
        try:
            #self._socket.bind((socket.gethostbyname('localhost'), 1883))
            self._socket.connect((host_ip, 1883))
        except socket.error:
            traceback.print_exc()
        #self._socket.connect((host_ip, 1883))

    def send(self):
        self._socket.send(bytearray("saidjsd"))
