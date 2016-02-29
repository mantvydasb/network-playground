from scapy.all import *

a = IP()
a.src = "192.168.2.2"
a.dst = "192.168.2.3"
hexdump(a)
print(a)