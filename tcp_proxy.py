import socket
import threading
import sys

LOCAL_ADDRESS = "192.168.2.2", 5555
LOCAL_ADDRESS = "127.0.0.1", 5555

def initVariables(self):
    arguments = sys.argv[1:]
    argumentsCount = len(arguments)

    if argumentsCount != 5:
        print("Usage: [localHost] [localPort] [remoteHost] [remotePort] [receiveFirst]")
    else:
        localHost = sys.argv[1]
        localPort = sys.argv[2]
        remoteHost = sys.argv[3]
        remotePort = sys.argv[4]
        shouldReceiveFirst = sys.argv[5]
        return localHost, localPort, remoteHost, remotePort, shouldReceiveFirst

def startListening(localHost, localPort, remoteHost, remotePort, shouldReceiveFirst):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(localHost, localPort)
    server.listen(5)
    print ("Listening: " + localHost + " " + str(localPort))

    while True:
        clientSocket, address = server.accept()
        print("Incoming connection: " + str(address))
        proxyThread = threading.Thread(target=handleProxyTraffic, args=[clientSocket, localHost, localPort, remoteHost, remotePort, shouldReceiveFirst])
        proxyThread.start()

def handleProxyTraffic(clientSocket, localHost, localPort, remoteHost, remotePort, shouldReceiveFirst):
    remoteSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remoteSocket.connect(remoteHost, remotePort)

    if shouldReceiveFirst:
        remoteBuffer = receiveFrom(remoteSocket)
        hexdump(remoteBuffer)
        remoteBuffer = modifyRemoteBuffer(remoteBuffer, remoteHost)
        remoteBufferLength = len(remoteHost)

        if remoteBufferLength:
            print("Sending %d bytes to localhost", remoteBufferLength)
            clientSocket.send(remoteBuffer)

        while True:
            localBuffer = receiveFrom(clientSocket)


def modifyRemoteBuffer(remoteBuffer, remoteHost):
    print("Buffer destined to " + "got modified.")
    return remoteBuffer

def modifyLocalBuffer(localBuffer, localHost):
    print("Buffer destined to " + "got modified.")
    return localBuffer

def hexdump(remoteBuffer):
    print("Dumping HEX for remote buffer")

def receiveFrom(remoteSocket):
    print("stuff")

def main():
    # localHost, localPort, remoteHost, remotePort, shouldReceiveFirst = initVariables()
    startListening(initVariables())
