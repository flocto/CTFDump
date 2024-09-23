# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: client.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2024-09-17 17:47:38 UTC (1726595258)

import sys
import socket
import time
import math
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
file = sys.argv[1]
ip = sys.argv[2]
port = 22993
with open(file, 'rb') as r:
    data_bytes = r.read()
current_time = time.time()
current_time = math.floor(current_time)
key_bytes = str(current_time).encode('utf-8')
init_key_len = len(key_bytes)
data_bytes_len = len(data_bytes)
temp1 = data_bytes_len // init_key_len
temp2 = data_bytes_len % init_key_len
key_bytes *= temp1
key_bytes += key_bytes[:temp2]
encrypt_bytes = bytes((a ^ b for a, b in zip(key_bytes, data_bytes)))
s.connect((ip, port))
s.send(encrypt_bytes)