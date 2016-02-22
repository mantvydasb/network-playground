from ctypes import *
import struct
import socket

class IPHeaderBuilder(Structure):
    _fields_ = [
        ("ihl", c_ubyte, 4),
        ("version", c_ubyte, 4),
        ("tos", c_ubyte),
        ("len", c_ushort),
        ("id", c_ushort),
        ("offset", c_ushort),
        ("ttl", c_ubyte),
        ("protocol_num", c_byte),
        ("sum", c_ushort),
        ("src", c_ulong),
        ("dst", c_ulong),
    ]

    def __init__(self, packedBytes):
        protocolMap = {1: "ICMP", 6: "TCP", 17: "UDP"}
        ipHeader = struct.unpack('BBHHHBBH4s4s', packedBytes)
        # ipHeader = (69, 32, 39169, 43119, 64, 114, 6, 40788, '(qW\xdc', '\xc0\xa8\x02\x02')
        self.sourceAddress = socket.inet_ntoa(ipHeader[8])
        self.destinationAddress = socket.inet_ntoa(ipHeader[9])
        self.protocol = protocolMap[ipHeader[6]]
