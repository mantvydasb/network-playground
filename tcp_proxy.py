import socket
import threading
import sys

# LOCAL_ADDRESS = "192.168.2.2", 5555
# LOCAL_ADDRESS = "127.0.0.1", 5555

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
    print ("Listening: " + localHost + " " + str(localPort))

    while True:
        clientSocket, address = server.accept()
        print("Incoming connection: " + str(address))
        # distributeTraffic(clientSocket, localHost, localPort, remoteHost, remotePort, True)
        proxyThread = threading.Thread(target=distributeTraffic, args=(clientSocket, localHost, localPort, remoteHost, remotePort, shouldReceiveFirst))
        proxyThread.start()
        clientSocket.send(b'Welcome to Pienas server @ 5555. Connection acknowledged.')

def receiveFrom(socket):
    buffer = ""
    # socket.settimeout(2)

    try:
        while True:
            data = socket.recv(4096)
            if not data: break
            else: buffer += data
    except: pass
    return buffer

def distributeTraffic(clientSocket, localHost, localPort, remoteHost, remotePort, shouldReceiveFirst):
    remoteSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remoteSocket.connect((remoteHost, int(remotePort)))

    # # read from remote -> send to local;
    # if shouldReceiveFirst:
    #     remoteBuffer = receiveFrom(remoteSocket)
    #     hexdump(remoteBuffer)
    #     remoteBuffer = modifyRemoteBuffer(remoteBuffer)
    #     remoteBufferLength = len(remoteHost)
    #
    #     if remoteBufferLength:
    #         print("Sending %d bytes to localhost" % remoteBufferLength)
    #         clientSocket.send(remoteBuffer.encode("utf8"))
    #
    # # read from local -> send to remote;
    # while True:
    #     localBuffer = receiveFrom(clientSocket)
    #     localBufferLength = len(localBuffer)
    #
    #     if localBufferLength:
    #         print("Received %d bytes from localhost" % localBufferLength)
    #         hexdump(localBuffer)
    #         localBuffer = modifyLocalBuffer(localBuffer)
    #         remoteSocket.send(localBuffer)
    #         print("Sent to remote")
    #
    #     remoteBuffer = receiveFrom(remoteSocket)
    #
    #     if len(remoteBuffer):
    #         print("Received %d bytes from remote" % len(remoteBuffer))
    #         hexdump(remoteBuffer)
    #         remoteBuffer = modifyRemoteBuffer(remoteBuffer)
    #         clientSocket.send(remoteBuffer)
    #         print("Send to localhost")

        # if not localBufferLength or not len(remoteBuffer):
        #     clientSocket.close()
        #     remoteSocket.close()
        #     break

def modifyRemoteBuffer(remoteBuffer):
    print("Buffer destined to remote host " + "got modified.")
    return remoteBuffer

def modifyLocalBuffer(localBuffer):
    print("Buffer destined to local host" + "got modified.")
    return localBuffer

def hexdump(source, length=16):
    print("Dumping HEX for remote buffer")
    result = []
    digits = 4
    # digits = 4 if isinstance(source, unicode) else 2

    for i in range(0, len(source), length):
        s = source[i:i + length]
        hexa = b' '.join(["%0*X" % (digits, ord(x)) for x in s])
        text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
        result.append(b"%04X    %-*s %s" % (i, length * (digits + i), hexa, text) )

        print(b'\n'.join(result))

def main():
    localHost, localPort, remoteHost, remotePort, shouldReceiveFirst = initVariables()
    startListening(localHost, localPort, remoteHost, remotePort, shouldReceiveFirst)

main()