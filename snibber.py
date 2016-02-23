import socket
import os
import subprocess
import ip_header_builder

PROMISCUOUS_MODE = "ip link set enp0s31f6 promisc "

class Snibber:
    host = "192.168.2.2"

    def __init__(self):
        snifferSocket = self.startListening()
        self.setPromiscuousOn()
        self.startSniffing(snifferSocket)

    def startSniffing(self, snifferSocket):
        while True:
            receivedPacket = snifferSocket.recvfrom(65565)
            # print("Received packet: " + str(receivedPacket))

            ipHeader = ip_header_builder.IPHeaderBuilder(receivedPacket[0])
            print("Protocol: %s, Src: %s, Dst: %s" % (str(ipHeader.protocol), str(ipHeader.sourceAddress), str(ipHeader.destinationAddress)))

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
        # sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        sniffer.bind((self.host, 0))
        print("[ # ] Snibber bound to %s" % self.host)
        return sniffer

    def getSocketProtocol(self):
        socketProtocol = ""
        if self.isThiswindows():
            socketProtocol = socket.IPPROTO_IP
        else:
            socketProtocol = socket.IPPROTO_TCP
        self.socketProtocol = socketProtocol
        return socketProtocol

snibber = Snibber()

