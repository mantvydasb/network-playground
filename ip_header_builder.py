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

    def __init__(self):
        self.protocolMap = {1: "ICMP", 6: "TCP", 17: "UDP"}
        self.sourceAddress = socket.inet_ntoa(struct.pack("<L", self.src))
        self.destinationAddress = socket.inet_ntoa(struct.pack("<L", self.dst))
        self.protocol = self.protocolMap[self.protocol_num]
        return self
