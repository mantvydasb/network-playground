import socket
import threading
import time

SERVER_ADDRESS = "192.168.2.2", 8506
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(SERVER_ADDRESS)
server.listen(5)

print ("# Simulating HTTP server on: " + SERVER_ADDRESS[0] + " " + str(SERVER_ADDRESS[1]))

def handleClient(clientSocket):
    while 1:
        data = clientSocket.recv(1024)
        if len(data):
            print("Received: " + str(data))
        else: break

while True:
    clientSocket, address = server.accept()
    print("Incoming connection: " + str(address))
    clientSocket.send(b'RESPONSE PACKET FROM THE WEBSERVER at ' + str(SERVER_ADDRESS).encode("utf8"))

    # while True:
    #     print("Sending a packet...")
    #     time.sleep(10)

    clientHandler = threading.Thread(target=handleClient, args=[clientSocket])
    clientHandler.start()
