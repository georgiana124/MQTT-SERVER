import socket

class Connection(object):

    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.settimeout(30)
        host_ip = socket.gethostbyname('iot.eclipse.org')
        self._socket.connect((host_ip, 1883))

