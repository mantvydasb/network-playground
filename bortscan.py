import socket
import threading
import sys

HOST = "192.168.2.2"
OPEN_PORTS = []

def main():
    if sys.argv[1]:
        HOST = sys.argv[1]

    print("Scanning %s for open ports in the range 0-65536" % HOST)
    for port in range(0, 65536):
        scanningThread = threading.Thread(target=scanPort, args=[HOST,port])
        scanningThread.start()

def scanPort(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        result = s.connect_ex((host, port))
        if result == 0: print("[!] Open: %s" % str(port))
    except: pass

main()