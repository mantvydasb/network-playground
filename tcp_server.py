import socket
import threading
import time

SERVER_ADDRESS = "192.168.2.2", 8506
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(SERVER_ADDRESS)
server.listen(5)

print ("# Simulating HTTP server on: " + SERVER_ADDRESS[0] + " " + str(SERVER_ADDRESS[1]))

def handleClient(clientSocket):
    print("handlinam clienta")
    while 1:
        print("handlinam clienta is loopo")
        data = clientSocket.recv(1024)
        if len(data):
            print("Received: " + str(data))
        else: break

while True:
    # clientSocket - l_address - simulated http server on 192.168.2.2 8506;
    # clientSocket - r_address - proxy server, which connected to our simulated http server on behalf of the client when firefox tried accessing a URL;
    clientSocket, address = server.accept()
    print("Incoming connection: " + str(address))
    clientSocket.send(b'RESPONSE PACKET FROM THE WEBSERVER at ' + str(SERVER_ADDRESS).encode("utf8"))

    clientHandler = threading.Thread(target=handleClient, args=[clientSocket])
    clientHandler.start()