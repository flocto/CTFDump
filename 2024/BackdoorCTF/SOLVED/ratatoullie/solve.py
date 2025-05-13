enc = b"x!8U\x19y\x11rz#o\x1f[9N4idqK"
key = bytes([8, 0x10, 0x42, 0x2f, 0x2d, 0xa, 0x3c, 0x46])

dec = bytes([e ^ key[i % len(key)] for i, e in enumerate(enc)])
print(dec.decode().upper())