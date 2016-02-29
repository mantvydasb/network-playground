from scapy.all import *

a = IP()
a.src = "192.168.2.2"
a.dst = "192.168.2.4"
print(a)

b = TCP()
print(b)

c = ARP()
c.op = 1
c.psrc = "192.168.2.50"
c.pdst = "192.168.2.60"
c.hwdst = "30:5a:3a:57:c0:50"

while True:
    print('Sending ARP packet:' + str(c))
    send(c)
    time.sleep(2)