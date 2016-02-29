import socket
import os
import subprocess
import ip_header_builder
from scapy.all import *


PROMISCUOUS_MODE = "ip link set enp0s31f6 promisc "
HOST = "192.168.2.2"
MAC_ADDRESS_REGEXP = '(([0-9a-zA-Z]+):){5}[0-9a-zA-Z]+'


class Snibber:

    def __init__(self):
        snifferSocket = self.startListening()
        self.setPromiscuousOn()
        self.startSniffing(snifferSocket)

    def startSniffing(self, snifferSocket):
        while True:
            receivedPacket = snifferSocket.recvfrom(65535)[0]
            IPheader = ip_header_builder.IPHeaderBuilder(receivedPacket, ip_header_builder.HEADER_TCP)

            if IPheader.data:
                print('\n\n\n############################################################')
                print("%s: %s:%s ===> %s:%s\nData: %s" % (str(IPheader.protocol), str(IPheader.sourceAddress), str(IPheader.sourcePort), str(IPheader.destinationAddress), str(IPheader.destinationPort), str(IPheader.data)))
                print('############################################################')
                self.isFTPlogin(IPheader)

    def setPromiscuousOn(self):
        self.setPromiscuousMode("on")

    def setPromiscuousOff(self):
        self.setPromiscuousMode("off")

    def setPromiscuousMode(self, mode):
        subprocess.Popen(PROMISCUOUS_MODE + mode, shell=True)

    def isThiswindows(self):
        return True if "nt" in os.name else False

    def startListening(self):
        sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, self.getSocketProtocol())
        sniffer.bind((HOST, 0))
        print("[ # ] Snibber bound to %s" % HOST)
        return sniffer

    def getSocketProtocol(self):
        if self.isThiswindows():
            self.socketProtocol = socket.IPPROTO_IP
        else:
            self.socketProtocol = socket.IPPROTO_TCP

        return self.socketProtocol

    def isFTPlogin(self, IPheader):
        packetData = IPheader.data.lower()
        if IPheader.destinationPort is 21 or IPheader.sourcePort is 21:
            if packetData.find("user") > -1 or packetData.find("pass") > -1:
                print("We have an attempt to login to FTP!\n" + IPheader.data)

snibber = Snibber()

