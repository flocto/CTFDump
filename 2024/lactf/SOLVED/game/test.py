data = [69, 70, -81, -117, -10, 109, 15, 29, 19, 113, 61, -123, -39, 82, -11, -34, 104, -98, -111, 9, 43, 35, -19, 22, 52, -55, -124, -45, -72, -23, 96, -77]

# normalize
from ctypes import c_uint8

data = [c_uint8(x).value for x in data]
hsh = bytes(data)

from hashlib import sha256

for i in range(256):
    b = bin(i)[2:].zfill(8)
    b = b.replace('0', 'p').replace('1', 'd')

    test = sha256(b.encode()).digest()
    if test == hsh:
        print(b)
        print(b.replace('d', '0').replace('p', '1'))
        break