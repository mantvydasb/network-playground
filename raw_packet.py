import socket
import struct
import time

NETWORK_INTERFACE   = 'enp0s31f6'

# Ethernet header
SOURCE_IP           = "192.168.2.2"
DESTINATION_IP      = "192.168.2.1"
SOURCE_MAC          = 0x30, 0x5a, 0x3a, 0x57, 0xc0, 0x2e
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
TOTAL_LENGTH        = 0 #will be set automatically by the OS;
IDENTIFICATION      = 0
FRAGMENT_OFFSET     = 0x4000  #also sets the "do not fragment packet flag
TIME_TO_LIVE        = 64
PROTOCOL_TCP        = 6
IP_HEADER_CHECKSUM     = 0, 0


# TCP header
DESTINATION_PORT    = 5555
SOURCE_PORT         = 55555
SEQUENCE_NUMBER     = 55
ACKNOWLDGEMENT_NUM  = 66
TCP_OFFSET = 5 << 4
TCP_FIN = 0
TCP_SYN = 1
TCP_RST = 0
TCP_PSH = 1
TCP_ACK = 1
TCP_URG = 0
TCP_FLAGS = TCP_FIN + (TCP_SYN << 1) + (TCP_RST << 2) + (TCP_PSH << 3) + (TCP_ACK << 4) + (TCP_URG << 5)
URGENT_POINTER = 0
WINDOW = socket.htons(0)
TCP_HEADER_CHECKSUM = 0

connection = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
connection.bind((('%s' % NETWORK_INTERFACE), socket.SOCK_RAW))

packet = [
    # Frame datagram
    struct.pack("!6B", *BROADCAST_MAC),
    struct.pack("!6B", *SOURCE_MAC),
    struct.pack("!H", TYPE_IP),

    # IP datagram
    struct.pack("!B", IP_VERSION_AND_HL),
    struct.pack("!B", SERVICE),
    struct.pack("!H", TOTAL_LENGTH),
    struct.pack("!H", IDENTIFICATION),
    struct.pack("!H", FRAGMENT_OFFSET),
    struct.pack("!B", TIME_TO_LIVE),
    struct.pack("!B", PROTOCOL_TCP),
    struct.pack("!BB", *IP_HEADER_CHECKSUM),
    socket.inet_aton(SOURCE_IP),
    socket.inet_aton(DESTINATION_IP),

    # TCP datagram
    struct.pack("!H", SOURCE_PORT),
    struct.pack("!H", DESTINATION_PORT),
    struct.pack("!L", SEQUENCE_NUMBER),
    struct.pack("!L", ACKNOWLDGEMENT_NUM),
    struct.pack("!B", TCP_OFFSET),
    struct.pack("!B", TCP_FLAGS),
    struct.pack("!H", WINDOW),
    struct.pack("!H", TCP_HEADER_CHECKSUM),
    struct.pack("!H", URGENT_POINTER),
    b'hello world, tis me - your first tcp packet'
]

counter = 0
while 1:
    print("Sending packet %s %s" % (str(counter), str(packet)))
    data = b'hello world'
    connection.send(b''.join(packet))
    time.sleep(.1)
    counter += 1
