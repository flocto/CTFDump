import scapy.all as scapy
import math

def decrypt(data_bytes, current_time):
    current_time = math.floor(current_time)
    key_bytes = str(current_time).encode('utf-8')
    init_key_len = len(key_bytes)
    data_bytes_len = len(data_bytes)
    temp1 = data_bytes_len // init_key_len
    temp2 = data_bytes_len % init_key_len
    key_bytes *= temp1
    key_bytes += key_bytes[:temp2]
    decrypt_bytes = bytes((a ^ b for a, b in zip(key_bytes, data_bytes)))
    return decrypt_bytes

pcap = scapy.rdpcap('Slingshot.pcapng')
# tcp.dstport == 22993

data = b''

for pkt in pcap:
    if pkt.haslayer(scapy.TCP) and pkt.haslayer(scapy.Raw):
        if pkt[scapy.TCP].dport == 22993:
            time = pkt.time
            dat = pkt[scapy.Raw].load
            data += decrypt(dat, time)

# print(data)
open('data.bin', 'wb').write(data)