import socket
import os
import subprocess
import ip_header_builder

PROMISCUOUS_MODE = "ip link set enp0s31f6 promisc "
HOST = "192.168.2.2"

class Snibber:
    def __init__(self):
        snifferSocket = self.startListening()
        self.setPromiscuousOn()
        self.startSniffing(snifferSocket)

    def startSniffing(self, snifferSocket):
        while True:
            receivedPacket = snifferSocket.recvfrom(65565)[0]
            ipHeader = ip_header_builder.IPHeaderBuilder(receivedPacket, ip_header_builder.HEADER_TCP)

            if ipHeader.data:
                print('\n\n\n############################################################')
                print("%s: %s:%s ===> %s:%s\nData: %s" % (str(ipHeader.protocol), str(ipHeader.sourceAddress), str(ipHeader.sourcePort), str(ipHeader.destinationAddress), str(ipHeader.destinationPort), str(ipHeader.data)))
                print('############################################################')

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

snibber = Snibber()

