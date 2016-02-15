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

def receiveFrom(remoteSocket):
    print("stuff")

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
            print("Sending %d bytes to localhost" % remoteBufferLength)
            clientSocket.send(remoteBuffer)

    # read from local -> send to remote;
    while True:
        localBuffer = receiveFrom(clientSocket)
        localBufferLength = len(localBuffer)

        if localBufferLength:
            print("Received %d bytes from localhost" % localBufferLength)
            hexdump(localBuffer)
            localBuffer = modifyLocalBuffer(localBuffer)
            remoteSocket.send(localBuffer)
            print("Sent to remote")

        remoteBuffer = receiveFrom(remoteSocket)

        if len(remoteBuffer):
            print("Received %d bytes from remote" % len(remoteBuffer))
            hexdump(remoteBuffer)
            remoteBuffer = modifyRemoteBuffer(remoteBuffer)
            clientSocket.send(remoteBuffer)
            print("Send to localhost")

        if not localBufferLength or not len(remoteBuffer):
            clientSocket.close()
            remoteSocket.close()
            break

def modifyRemoteBuffer(remoteBuffer):
    print("Buffer destined to " + "got modified.")
    return remoteBuffer

def modifyLocalBuffer(localBuffer):
    print("Buffer destined to " + "got modified.")
    return localBuffer

def hexdump(source, length=16):
    print("Dumping HEX for remote buffer")
    result = []
    digits = 4
    # digits = 4 if isinstance(source, unicode) else 2

    for i in range(0, len(source), length):
        s = source[i:i + length]
        hexa = b' '.join(["%0*X" % (digits, ord(x)) for x in s])




def main():
    # localHost, localPort, remoteHost, remotePort, shouldReceiveFirst = initVariables()
    startListening(initVariables())
