from ctypes import *
import struct
import socket

class IPHeaderBuilder():

    def __init__(self, packedBytes):
        protocolMap = {1: "ICMP", 6: "TCP", 17: "UDP"}
        ipHeader = struct.unpack('<bbHHHBBH4s4s', packedBytes[0:20])

        self.protocol = protocolMap[ipHeader[6]]
        self.sourceAddress = socket.inet_ntoa(ipHeader[8])
        self.destinationAddress = socket.inet_ntoa(ipHeader[9])
        self.data = ''

        versionIhl = ipHeader[0]
        version = versionIhl >> 4
        internetHeaderLength = versionIhl & 0xF
        IPheaderLength = internetHeaderLength * 4

        TCPheader = packedBytes[IPheaderLength:IPheaderLength + 20]
        TCPheaderUnpacked = struct.unpack('!HHLLBBHHH' , TCPheader)

        self.sourcePort = TCPheaderUnpacked[0]
        self.destinationPort = TCPheaderUnpacked[1]

        doffReserved = TCPheaderUnpacked[4]
        TCPlength = doffReserved >> 4

        # len(IPheader + TCP header lentgth * 4)
        dataOffset = 20 + TCPlength * 4
        self.dataSize = len(packedBytes) - dataOffset
        self.data = str(packedBytes[dataOffset:]).rstrip()