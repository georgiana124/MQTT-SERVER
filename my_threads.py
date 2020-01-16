from threading import Thread
from threading import Timer

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
