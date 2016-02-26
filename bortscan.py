import socket
import threading
import sys

def main():
    if len(sys.argv) > 1: host = sys.argv[1]
    else: host = "192.168.2.2"

    print("Scanning %s for open ports in the range 0-65536" % host)
    for port in range(0, 65536):
        scanningThread = threading.Thread(target=scanPort, args=[host,port])
        scanningThread.run()

def scanPort(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        result = s.connect_ex((host, port))
        if result == 0:
            print("[!] Open: %s" % str(port))
        s.close()
    except: pass

main()