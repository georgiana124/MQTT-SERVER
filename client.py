"""
default host
broker test host
iot.eclipse.org
port 1883
"""
import Connection as conn
import message_types as messages


class Client(object):

    def __init__(self, topic=None, username=None, password=None, keep_alive=60, message_retry=20):
        self._username = username
        self._password = password
        self._topic = topic
        self._connection = conn.Connection()
        self._keep_alive = keep_alive
        self._socket = None
        self._message_retry = message_retry
        self._in_packet = {
            "command": 0,
            "have_remaining": 0,
            "remaining_count": [],
            "remaining_mult": 0,
            "remaining_length": 0,
            "packet": b"",
            "pos": 0
        }
        self._thread = None

    def connect(self, host, port=1883, bind_address="", bind_port=0):
        """ Variable header represents 04MQTT in hex values"""
        VARIABLE_HEADER = 0x00044D515454

    def publish(self, dup=False, qos=0x01, retain=False):
        command = messages.PUBLISH | (dup & 0x1) << 3 | qos << 1 | retain
        command << 8
        packet = bytearray(0x0)
        packet.append(command)
        #print(packet)
        #self._connection.send()

    def subscribe(self):
        pass
