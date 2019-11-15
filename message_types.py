# Message types
CONNECT = 0x10
CONNACK = 0x20
PUBLISH = 0x30
PUBACK = 0x40
PUBREC = 0x50
PUBREL = 0x62
PUBCOMP = 0x70
SUBSCRIBE = 0x82
SUBACK = 0x90
UNSUBSCRIBE = 0xA2
UNSUBACK = 0xB0
PINGREQ = 0xC0
PINGRESP = 0xD0
DISCONNECT = 0xE0
AUTH = 0xF0


class PacketTypes(object):
    indexes = range(1, 16)
    # Packet types
    CONNECT, CONNACK, PUBLISH, PUBACK, PUBREC, PUBREL, \
    PUBCOMP, SUBSCRIBE, SUBACK, UNSUBSCRIBE, UNSUBACK, \
    PINGREQ, PINGRESP, DISCONNECT, AUTH = indexes

    # Dummy packet type for properties use - will delay only applies to will
    WILLMESSAGE = 99

    Names = ["reserved",
             "Connect", "Connack", "Publish", "Puback", "Pubrec", "Pubrel",
             "Pubcomp", "Subscribe", "Suback", "Unsubscribe", "Unsuback",
             "Pingreq", "Pingresp", "Disconnect", "Auth"]
