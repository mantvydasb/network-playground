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
            if "upload" in command:
                package = self.buildPackageForUpload(command)
            else:
                package = command.encode("utf8")
            self.clientSocket.send(package)
            self.handleServerResponse(self.clientSocket)

    def buildPackageForUpload(self, command):
        fileName, filePath = self.getFileNameAndPath(command)
        fileData = self.readFileData(filePath)
        return (UPLOAD_ANCHOR + fileName + "#").encode("utf8") + fileData

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
        clientRequest = ''
        receivedDataLength = 1
        blockSize = 1024

        while True:
            while receivedDataLength:
                receivedData = clientSocket.recv(blockSize).decode("utf8")
                receivedDataLength = len(receivedData)
                clientRequest += receivedData
                if (receivedDataLength < blockSize): break

            if "download" in clientRequest:
                package = self.buildPackageForDownload(clientRequest)
                clientSocket.send(package)

            elif "upload" in clientRequest:
                fileName, fileData = self.getFileNameAndFileData(clientRequest)
                self.saveToFile(fileName, fileData)
                print(fileName.rstrip() + " downloaded to " + os.getcwd())
                clientSocket.send(b'File uploaded!')
            else:
                clientSocket.send(self.executeCommand(clientRequest))
            print("Executing: " + clientRequest)

    def buildPackageForDownload(self, clientRequest):
        fileName, filePath = self.getFileNameAndPath(clientRequest)
        fileData = self.readFileData(filePath)
        package = (DOWNLOAD_ANCHOR + fileName + "#").encode("utf8") + fileData
        return package

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

            # am I being sent a file?! Well then save it!
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
        anchor = ''
        if DOWNLOAD_ANCHOR in response:
            anchor = DOWNLOAD_ANCHOR
        elif UPLOAD_ANCHOR in response:
            anchor = UPLOAD_ANCHOR
        fileData = response.strip(anchor).strip(fileName + "#")
        return fileName, fileData

kit = mnetkit()