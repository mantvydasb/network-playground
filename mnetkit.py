import sys
import socket
import getopt
import threading
import threading

LISTEN = False
COMMAND = False
UPLOAD_DESTINATION = ""
UPLOAD = False
EXECUTE = ""
TARGET = ""
PORT = 0

def usage():
    print("Welcome to MNetkit\n")
    print("Usage: mnetkit.py -t IP -p PORT [-lcueh]")
    print("-l                   Open up port for incoming connections on [IP]:[PORT]")
    print("-c                   Initialise a command shell")
    print("-u file_to_upload    Upload specified file to [IP]:[PORT]")
    print("-e file_to_run       Execute a command when connection is received. Example: mnetkit.py -t 192.168.55 -p 5555 -e /bin/bash")
    print("-h                   Display help/usage")
    sys.exit()

def main():
    if not len(sys.argv[1:]):
        usage()

main()