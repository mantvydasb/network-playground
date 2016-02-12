import sys
import socket
import getopt
import threading
import subprocess
import os


DOWNLOAD_ANCHOR = "#download#"
UPLOAD_ANCHOR = "#upload#"

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
        print("download /path/file  Download a file from remote machine")
        print("upload /path/file    Upload a file to remote machine")
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
                # print("Options: " + str(options) + "\n")
                # print("Arguments: " + str(arguments) + "\n")
                return options, arguments
            except getopt.GetoptError as error:
                print(str(error))
                self.displayUsage()

    def captureCommand(self):
        return input("mnetkit>")

    def connectToHost(self, host, port):
        remoteAddress = host, int(port)
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        clientSocket.connect(remoteAddress)
        return clientSocket

    def sendCommand(self):
        command = self.captureCommand()
        if (len(command) > 0):
            self.clientSocket.send(command.encode("utf8"))
            self.handleServerResponse(self.clientSocket)

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

    # server receives the request and processes it;
    def handleClientRequest(self, clientSocket):

        while True:
            clientRequest = clientSocket.recv(1024).decode("utf8")
            print("Executing: " + clientRequest)

            if "download" in clientRequest:
                fileName, filePath = self.getFileNameAndPath(clientRequest)
                fileData = self.readFileData(filePath)

                package = (DOWNLOAD_ANCHOR + fileName + "#").encode("utf8") + fileData
                clientSocket.send(package)

            # elif "upload" in clientRequest:
            #     fileName, filePath = self.getFileNameAndPath(clientRequest)
            #     fileData = self.readFileData(filePath)

            else:
                clientSocket.send(self.executeCommand(clientRequest))

    def readFileData(self, filePath):
        return self.executeCommand("cat " + filePath)

    def getFileNameAndPath(self, clientRequest):
        filePath = clientRequest[clientRequest.find(" ") + 1:]
        brokenDownPath = filePath.split("/")
        fileName = brokenDownPath[len(brokenDownPath) - 1].strip('"')
        return fileName, filePath

    # client receives the response for the request sent earlier;
    def handleServerResponse(self, client):
        blockSize = 1024
        response = ""
        receivedDataLength = 1

        while True:
            while receivedDataLength:
                receivedData = client.recv(blockSize).decode("utf8")
                receivedDataLength = len(receivedData)
                response += receivedData
                if receivedDataLength < blockSize: break

            # was request to download a file?
            if DOWNLOAD_ANCHOR in response:
                fileName, response = self.getFileNameAndFileData(response)
                self.saveToFile(fileName, response)
                print(fileName.rstrip() + " downloaded to " + os.getcwd())
            # print response;
            else:
                print("\n" + response)

            self.sendCommand()

    def saveToFile(self, fileName, fileData):
        file = open(fileName, mode="w+")
        file.write(fileData)
        file.close()

    def getFileNameAndFileData(self, response):
        fileName = response.split("#")[2]
        response = response.strip(DOWNLOAD_ANCHOR).strip(fileName + "#")
        return fileName, response

kit = mnetkit()