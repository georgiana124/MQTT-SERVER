class Packet:

    def __init__(self):
        self.packet_fields = {
            'protocol_name': "MQTT",
            'keep_alive': b'\x00\x05',  # keep alive
            'properties': b'\x11\x00\x00\x00\x0a',  # properties
            'connect_flags': b'\x02',  # connect flags
            'version': b'\5'
        }

    def parse(self):
        pass


class Connect(Packet):

    def parse(self):
        return None


class Disconnect(Packet):

    def parse(self):
        return 0


class Publish(Packet):

    def parse(self):
        a = self.packet_fields['version']
        return a


class Subscribe(Packet):

    def parse(self):
        return 0


class Unsubscribe(Packet):

    def parse(self):
        return 0
