import socket

TARGET = "127.0.0.1", 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(TARGET)
client.send(b'SYN/ACK')
