import sys
import socket
import getopt
import threading
import subprocess

class mnetkit():
    LISTEN = False
    COMMAND = False
    UPLOAD_DESTINATION = ""
    UPLOAD = False
    EXECUTE = ""
    TARGET = None
    PORT = 0

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

        if not self.LISTEN and (self.TARGET is not None or self.PORT > 0):
            self.captureCommandAndSend()
        elif self.LISTEN:
            print ("Listening...")
            self.startListening()

    def captureCommandAndSend(self):
        buffer = input("mnetkit>")
        self.send(str(buffer))
        print("Command captured: " + buffer)

    def send(self, buffer):
        remoteAddress = self.TARGET, int(self.PORT)
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect(remoteAddress)

        if (buffer.__len__() > 0):
            clientSocket.send(buffer.encode("utf8"))
            self.receiveResponse(clientSocket)

    def startListening(self):
        if not (self.TARGET):
            self.TARGET = "192.168.2.2"

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.TARGET, int(self.PORT)))
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

        if len(self.UPLOAD_DESTINATION):
            file = open(self.UPLOAD_DESTINATION, "r")
            fileContent = file.read()
            print("File content: " + fileContent)
            fileBuffer = ""
            clientSocket.send(fileContent.encode("utf8"))

            while True:
                data = clientSocket.recv(1024)
                if not data: break
                else:
                    fileBuffer += data.decode("utf8")
            try:
                # file = open(self.UPLOAD_DESTINATION, "wb")
                file = open('~/Desktop/mnnekit2.py', "wb")
                file.write(fileBuffer)
                file.close()
                clientSocket.send(b'File uploaded successfully')
            except:
                print("Failed to upload file..")

    def receiveResponse(self, client):
        response = ""
        data = client.recv(4096)

        while data:
            response += data.decode("utf8")
            print("Response: " + response)
            self.captureCommandAndSend()

    def initialiseSwitches(self, options):
        for (option, argument) in options:
            if option in ("-h"):
                self.displayUsage()
            if option in ("-l"):
                self.LISTEN = True
            if option in ("-e"):
                self.EXECUTE = argument
            if option in ("-u"):
                self.UPLOAD_DESTINATION = argument
                print("Got file to upload: " + self.UPLOAD_DESTINATION)
            if option in ("-t"):
                self.TARGET = argument
            if option in ("-p"):
                self.PORT = argument

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

kit = mnetkit()
