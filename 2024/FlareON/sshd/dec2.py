from chacha20_python3 import chacha20_encrypt

enc = b'\xa9\xf64\x08B*\x9e\x1c\x0c\x03\xa8\x08\x94p\xbb\x8d\xaa\xdcm{$\xff\x7f$|\xda\x83\x9e\x92\xf7\x07\x1d\x02c\x90.\xc1X'
key = b'\x8d\xec\x91\x12\xebv\x0e\xda|}\x87\xa4C\'\x1c5\xd9\xe0\xcb\x87\x89\x93\xb4\xd9\x04\xae\xf94\xfa!f\xd7'
nonce = b'\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11\x11'

dec = chacha20_encrypt(enc, key, nonce)
print(dec)