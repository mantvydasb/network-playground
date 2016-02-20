import socket
import threading
import sys

LOCAL_HOST = "192.168.2.2"
LOCAL_PORT = 8084

def initVariables():
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
    server.bind((localHost, int(localPort)))
    server.listen(5)
    print ("[ # ] Simulating proxy server " + str(server.getsockname()))

    while True:
        clientSocket, address = server.accept()
        print("[ < ] FTP client %s connected to proxy %s " % (str(address), str(server.getsockname())))
        proxyThread = threading.Thread(target=distributeTraffic, args=(clientSocket, localHost, localPort, remoteHost, remotePort, shouldReceiveFirst))
        proxyThread.start()

def receiveFrom(socket):
    while 1: return socket.recv(4098)

def distributeTraffic(ftpClientSocket, localHost, localPort, remoteHost, remotePort, shouldReceiveFirst):
    ftpServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ftpServerSocket.connect((remoteHost, int(remotePort)))
    print("[ > ] Proxy %s connected to FTP server " % str(ftpServerSocket.getsockname()))

    while True:
        # remote data going through proxy to local socket
        remoteBuffer = receiveFrom(ftpServerSocket)
        remoteBufferLength = len(remoteBuffer)

        if remoteBufferLength:
            remoteBufferDecoded = remoteBuffer.decode("utf8").rstrip()
            print("[ < ] Proxy %s received from FTP server" % str(ftpServerSocket.getsockname()) + ": '" + remoteBufferDecoded + "' [" + str(remoteBufferLength) + " bytes]")
            ftpClientSocket.send(remoteBuffer)
            print("[ > ] Proxy %s sent '%s' to FTP client %s " % ( (str(ftpClientSocket.getsockname()), remoteBufferDecoded, str(ftpClientSocket.getpeername()))))

        # local data going through proxy to remote socket
        localBuffer = receiveFrom(ftpClientSocket)
        localBufferDecoded = localBuffer.decode("utf8").rstrip()

        if len(localBuffer):
            print("[ < ] Proxy %s received '%s' from FTP client %s" % (str(ftpClientSocket.getsockname()), localBufferDecoded, str(ftpClientSocket.getpeername())))
            ftpServerSocket.send(localBuffer)
            print("[ > ] Proxy %s sent '%s' to FTP server: " %(str(ftpServerSocket.getsockname()), localBufferDecoded))



def modifyRemoteBuffer(remoteBuffer):
    return remoteBuffer

def modifyLocalBuffer(localBuffer):
    return localBuffer

def hexdump(source, length=16):
    print("Dumping HEX for remote buffer")
    print(source)

def main():
    # localHost, localPort, remoteHost, remotePort, shouldReceiveFirst = initVariables()
    localHost = LOCAL_HOST
    localPort = LOCAL_PORT
    remoteHost = "192.168.2.2"
    remotePort = 21
    shouldReceiveFirst = True
    startListening(localHost, localPort, remoteHost, remotePort, shouldReceiveFirst)

main()