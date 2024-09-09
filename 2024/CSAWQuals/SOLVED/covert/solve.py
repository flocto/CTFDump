from scapy.all import *
from math import gcd
from functools import reduce

def gcd_list(numbers):
    return reduce(gcd, numbers)

pcap = rdpcap('parsed.pcapng')

dat = []
for pkt in pcap:
    if not pkt.haslayer(IP):
        continue
    ip_id = pkt[IP].id
    
    if ip_id % 5 == 0 and ip_id > 1000 and ip_id < 10000:
        dat.append(ip_id)

dat = dat[1:] # truncate

g = gcd_list(dat)
print(dat, g)

print(bytes([x // g for x in dat]))