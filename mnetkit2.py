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
            self.receiveResponse(self.clientSocket)
            self.sendCommand()

    def startListening(self):
        print ("Listening on " + self.HOST + ":" + str(self.PORT))
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.HOST, int(self.PORT)))
        server.listen(5)

        while True:
            clientSocket, clientAddress = server.accept()
            print("Incoming connection..")
            clientThread = threading.Thread(target=self.handleClientRequest, args=[clientSocket])
            clientThread.start()

    def executeCommand(self, command):
        command = command.rstrip()
        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        except:
            output = "Failed to execute command!".encode("utf8")
        return "Command did not return any data".encode("utf8") if not output else output

    def handleClientRequest(self, clientSocket):
        response = ""
        while True:
            data = clientSocket.recv(1024).decode("utf8")
            if data:
                response += data
                print("Executing: " + data)
                clientSocket.send(self.executeCommand(data))
            else:
                response = ""

    def receiveResponse(self, client):
        blockSize = 1024
        response = ""
        receivedDataLength = 1

        while True:
            while receivedDataLength:
                receivedData = client.recv(blockSize).decode("utf8")
                receivedDataLength = len(receivedData)
                response += receivedData
                if receivedDataLength < blockSize: break
            print("\n" + response)
            self.sendCommand()


kit = mnetkit()

# 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