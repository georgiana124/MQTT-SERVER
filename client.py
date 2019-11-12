
class Client(object):
    topic = ""
    username = ""
    password = ""

    def __init__(self, _topic, _username, _password):
        self.username = _username
        self.password = _password
        self.topic = _topic

    def connect(self):
        """ Variable header represents 04MQTT in hex values"""
        variableHeader= 0x00044D515454



    def publish(self):

    def subscribe(self):

