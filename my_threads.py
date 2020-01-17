from threading import Thread
from threading import Timer
import queue
packet_pub = queue.Queue()

""" This class implements a scheduler for sending a pingreq packet. 
    It is scheduled to send a ping request every n seconds, based on the keep alive flag. """
class Ping_Thread:

    def __init__(self, _keep_alive, _target):
        self.target = _target
        self.is_running = False
        self.keep_alive = _keep_alive
        self.timer = None
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.target()

    def start(self):
        if not self.is_running:
            self.timer = Timer(self.keep_alive, self._run)

            self.timer.start()
            self.is_running = True

    def stop(self):
        self.timer.cancel()
        self.is_running = False

class Receive_Message:

    def __init__(self, _timer, _target):
        self.target = _target
        self.target2 = None
        self.is_subscribed = False
        self.timer = _timer
        self.timer_thread = None

    def set_target_2(self, _target):
        self.target2 = _target

    def _run(self):
        self.is_subscribed = False
        self.start()
        packet = self.target(1024)

        if packet[0:1] == b'\x30':
            length_remain = int.from_bytes(packet[1:2], 'big')
            topic_length = int.from_bytes(packet[2:4], 'big') - 1
            length_remain = length_remain - topic_length
            message = packet[length_remain:].decode('UTF-8')
            self.target2(message)

    def start(self):
        if not self.is_subscribed:
            self.timer_thread = Timer(self.timer, self._run)
            self.timer_thread.start()
            self.is_subscribed = True

    def stop(self):
        self.timer_thread.cancel()
        self.is_subscribed = False
