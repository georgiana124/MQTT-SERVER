from packets import Packet


class Disconnect(Packet):

    def parse(self):
        return 0
