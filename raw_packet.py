import socket
import struct
import time

NETWORK_INTERFACE   = 'enp0s31f6'

# Ethernet header
SOURCE_IP           = "192.168.2.2"
DESTINATION_IP      = "192.168.2.1"
SOURCE_MAC          = [0x30, 0x5a, 0x3a, 0x57, 0xc0, 0x2e]
DESTINATION_MAC     = "00:1c:df:c1:bd:91"
BROADCAST_MAC       = [0xFF]*6
HARDWARE_SIZE       = 0x0006
PROTOCOL_SIZE       = 0x0004

#ARP
TYPE_ARP            = 0x0806
OPERATION           = 0x0002

# IP header
TYPE_IP             = 0x0800
IP_VERSION_AND_HL   = 0x45
SERVICE             = 0
TOTAL_LENGTH        = (IP_VERSION_AND_HL >> 4) * 5
IDENTIFICATION      = 0
FRAGMENT_OFFSET     = 0
TIME_TO_LIVE        = 64
PROTOCOL_TCP        = 6
HEADER_CHECKSUM     = 0, 0

connection = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
connection.bind((('%s' % NETWORK_INTERFACE), socket.SOCK_RAW))

packet = [
    # Frame header
    struct.pack("!6B", *BROADCAST_MAC),
    struct.pack("!6B", *SOURCE_MAC),
    struct.pack("!H", TYPE_IP),

    # IP header
    struct.pack("!B", IP_VERSION_AND_HL),
    struct.pack("!B", SERVICE),
    struct.pack("!H", TOTAL_LENGTH),
    struct.pack("!H", IDENTIFICATION),
    struct.pack("!H", FRAGMENT_OFFSET),
    struct.pack("!B", TIME_TO_LIVE),
    struct.pack("!B", PROTOCOL_TCP),
    struct.pack("!BB", *HEADER_CHECKSUM),
    socket.inet_aton(SOURCE_IP),
    socket.inet_aton(DESTINATION_IP),
]

while 1:
    print("Sending packet %s" % str(packet))
    connection.send(b''.join(packet))
    time.sleep(.1)



