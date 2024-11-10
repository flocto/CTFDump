import scapy.all as scapy

pcap = scapy.rdpcap("capture.pcapng")

dat = b''

for pkt in pcap:
    if pkt.haslayer(scapy.Raw):
        dat += pkt[scapy.Raw].load

print(dat[48*4:])