import socket
import threading

SERVER_ADDRESS = "127.0.0.1", 5555
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(SERVER_ADDRESS)
server.listen(5)

print ("Listening: " + SERVER_ADDRESS[0] + " " + str(SERVER_ADDRESS[1]))

def handleClient(clientSocket):
    request = clientSocket.recv(1024)
    print("Received: " + str(request))
    clientSocket.send(b'ACK')
    clientSocket.close()

while True:
    client, address = server.accept()
    print("Incoming connection: " + str(address))
    clientHandler = threading.Thread(target=handleClient, args=[client])
    clientHandler.start()