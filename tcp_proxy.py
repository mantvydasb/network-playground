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
    server.bind((localHost, localPort))
    server.listen(5)
    print ("Listening: " + localHost + " " + str(localPort))

    while True:
        clientSocket, address = server.accept()
        print("Incoming connection: " + str(address))
        proxyThread = threading.Thread(target=distributeTraffic, args=[clientSocket, localHost, localPort, remoteHost, remotePort, shouldReceiveFirst])
        proxyThread.start()

def distributeTraffic(clientSocket, localHost, localPort, remoteHost, remotePort, shouldReceiveFirst):
    remoteSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remoteSocket.connect(remoteHost, remotePort)

    # read from remote -> send to local;
    if shouldReceiveFirst:
        remoteBuffer = receiveFrom(remoteSocket)
        hexdump(remoteBuffer)
        remoteBuffer = modifyRemoteBuffer(remoteBuffer)
        remoteBufferLength = len(remoteHost)

        if remoteBufferLength:
            print("Sending %d bytes to localhost", remoteBufferLength)
            clientSocket.send(remoteBuffer)

    # read from local -> send to remote;
    while True:
        localBuffer = receiveFrom(clientSocket)
        localBufferLength = len(localBuffer)

        if localBufferLength:
            print("Received %d bytes from localhost", localBufferLength)
            hexdump(localBuffer)
            localBuffer = modifyLocalBuffer(localBuffer)
            remoteSocket.send(localBuffer)
            print("Sent to remote")

        remoteBuffer = receiveFrom(remoteSocket)



def modifyRemoteBuffer(remoteBuffer):
    print("Buffer destined to " + "got modified.")
    return remoteBuffer

def modifyLocalBuffer(localBuffer):
    print("Buffer destined to " + "got modified.")
    return localBuffer

def hexdump(buffer):
    print("Dumping HEX for remote buffer")

def receiveFrom(remoteSocket):
    print("stuff")

def main():
    # localHost, localPort, remoteHost, remotePort, shouldReceiveFirst = initVariables()
    startListening(initVariables())
