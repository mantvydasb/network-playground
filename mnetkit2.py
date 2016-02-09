import sys
import socket
import getopt
import threading
import subprocess

class mnetkit():
    COMMAND = False
    UPLOAD_DESTINATION = ""
    EXECUTE = ""
    HOST = None
    PORT = 0
    clientSocket = ""

    def displayUsage(self):
        print("Welcome to MNetkit\n")
        print("Usage: mnetkit.py -t IP -p PORT [-options]")
        print("-l                   Open up port for incoming connections on [IP]:[PORT]")
        print("-c                   Initialise a command shell")
        print("-u file_to_upload    Upload specified file to [IP]:[PORT]")
        print("-e file_to_run       Execute a command when connection is received. Example: mnetkit.py -t 192.168.55 -p 5555 -e /bin/bash")
        print("-h                   Display help/usage")
        sys.exit()

    def __init__(self):
        options, arguments = self.parseArguments()
        self.initialiseSwitches(options)

    def initialiseSwitches(self, options):
        isListening = False

        for (option, argument) in options:
            if option in ("-h"):
                self.displayUsage()
            # defines if this instance is a server (-l) or a client
            if option in ("-l"):
                isListening = True
                self.startListening()
            if option in ("-t"):
                self.HOST = argument
            if option in ("-p"):
                self.PORT = argument
            if option in ("-e"):
                self.EXECUTE = argument
            if option in ("-u"):
                self.UPLOAD_DESTINATION = argument

        if not isListening and self.HOST:
            self.clientSocket = self.connectToHost(self.HOST, self.PORT)
            self.sendCommand()

    def parseArguments(self):
        arguments = sys.argv[1:]
        argumentsCount = len(arguments)

        if argumentsCount <= 0:
            self.displayUsage()
        else:
            try:
                options, arguments = getopt.getopt(arguments, "hle:t:p:c:u:")
                print("Options: " + str(options) + "\n")
                print("Arguments: " + str(arguments) + "\n")
                return options, arguments
            except getopt.GetoptError as error:
                print(str(error))
                self.displayUsage()

    def captureCommand(self):
        return input("mnetkit>")

    def connectToHost(self, host, port):
        remoteAddress = host, int(port)
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect(remoteAddress)
        return clientSocket

    def sendCommand(self):
        command = self.captureCommand()
        if (command.__len__() > 0):
            self.clientSocket.send(command.encode("utf8"))
            self.sendCommand()
            self.receiveResponse(self.clientSocket)

    def startListening(self):
        print ("Listening on " + self.HOST + ":" + str(self.PORT))
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.HOST, int(self.PORT)))
        server.listen(5)

        while True:
            clientSocket, clientAddress = server.accept()
            print("Incoming connection..")
            clientSocket.send(b'SYN/ACK')
            clientThread = threading.Thread(target=self.handleClientRequest, args=[clientSocket])
            clientThread.start()

    def executeCommand(self, command):
        command = command.rstrip()
        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        except:
            output = "Failed to execute command!"
        return output

    def handleClientRequest(self, clientSocket):
        response = ""
        while True:
            data = clientSocket.recv(1024)
            if data:
                response += data.decode("utf8")
                print("Received command: " + response)

    def receiveResponse(self, client):
        response = ""

        while True:
            data = client.recv(4096)
            if data:
                response += data.decode("utf8")
                print("Response: " + response)

kit = mnetkit()
