import socket
import os
import subprocess

PROMISCUOUS_CMD_BASE = "ip link set enp0s31f6 promisc "

class snibber:
    host = "192.168.2.2"

    def __init__(self):
        snifferSocket = self.startListening()
        self.setPromiscOn()

        while True:
            print(snifferSocket.recvfrom(65565))

    def setPromiscOn(self):
        subprocess.Popen(PROMISCUOUS_CMD_BASE + "on", shell=True)

    def setPromiscOff(self):
        subprocess.Popen(PROMISCUOUS_CMD_BASE + "off", shell=True)

    def isThiswindows(self):
        return True if "nt" in os.name else False

    def startListening(self):
        sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, self.getSocketProtocol())
        sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        sniffer.bind((self.host, 0))
        print("[ # ] Snibber bound to %s" % self.host)
        return sniffer

    def getSocketProtocol(self):
        socketProtocol = ""
        if self.isThiswindows():
            socketProtocol = socket.IPPROTO_IP
        else:
            socketProtocol = socket.IPPROTO_ICMP
        self.socketProtocol = socketProtocol
        return socketProtocol

    def startSniffing(self):
        print()


snibber = snibber()

