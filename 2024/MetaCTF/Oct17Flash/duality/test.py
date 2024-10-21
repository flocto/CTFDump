from Crypto.Util.number import * 
from os import urandom

for i in range(100):
    w = bytes_to_long(urandom(10))
    print(w, w.bit_length())