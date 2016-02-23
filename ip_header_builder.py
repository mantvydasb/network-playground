from ctypes import *
import struct
import socket

class IPHeaderBuilder():
    def __init__(self, packedBytes):
        protocolMap = {1: "ICMP", 6: "TCP", 17: "UDP"}
        ipHeader = struct.unpack('<bbHHHBBH4s4s', packedBytes[0:20])
        # print("IP header:" + str(ipHeader))
        # ipHeader = struct.unpack('BBHHHBBH4s4s', packedBytes)
        # ipHeader = (b8-version-69, b-IHL-32, h-TOS-39169, h-totallength-43119, h-idenfification-64, b-flags-114, b6, h40788, '4s-sourceaddress-qW\xdc, 4s-destaddress-\xc0\xa8\x02\x02'

        self.protocol = protocolMap[ipHeader[6]]
        self.sourceAddress = socket.inet_ntoa(ipHeader[8])
        self.destinationAddress = socket.inet_ntoa(ipHeader[9])
        self.data = ''

        version_ihl = ipHeader[0]
        version = version_ihl >> 4
        ihl = version_ihl & 0xF
        iph_length = ihl * 4

        tcp_header = packedBytes[iph_length:iph_length+20]

        tcph = struct.unpack('!HHLLBBHHH' , tcp_header)
        source_port = tcph[0]
        dest_port = tcph[1]
        sequence = tcph[2]
        acknowledgement = tcph[3]
        doff_reserved = tcph[4]
        tcph_length = doff_reserved >> 4

        print('Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Sequence Number : ' + str(sequence) + ' Acknowledgement : ' + str(acknowledgement) + ' TCP header length : ' + str(tcph_length))
        h_size = 20 + tcph_length * 4
        data_size = len(packedBytes) - h_size
        data = packedBytes[h_size:]
        print('Data : ' + data)
