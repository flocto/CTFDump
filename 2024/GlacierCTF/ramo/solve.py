from Crypto.Cipher import AES
import struct

def gen_printable(len, seed):
    R = seed
    result = bytearray(len)
    if len <= 0:
        result[len] = 0
        return result

    i = 0
    while i < len:
        R = R * 0x343fd + 0x269ec3
        R = R & 0xFFFFFFFF
        result[i] = ((R >> 0x10) & 0x7fff) % 94 + 0x20
        i += 1

    # result[len] = 0
    return result, R

def brute_seed_part(n):
    fname = b'flag.txt'
    for i in range(256):
        v = i + 0x1505
        for c in fname:
            v = v * 0x21 + c
            v = v & 0xFFFFFFFF
        if v == n:
            return i
    return -1

dat = open('flag.txt.enc', 'rb').read()
enc = b''

seeds = []
for i in range(0, len(dat), 0x10 + 4):
    chunk = dat[i:i + 0x10 + 4]
    seed = struct.unpack('<I', chunk[:4])[0]
    seeds.append(seed)
    enc += chunk[4:]

print(seeds, enc)

seeds = [brute_seed_part(seed) for seed in seeds]
seed = struct.unpack('<I', bytearray(seeds))[0]
print(hex(seed))

key, seed = gen_printable(0x20, seed)
key = key[:0x10]
iv, seed = gen_printable(0x10, seed)

print(key, iv)

cipher = AES.new(key, AES.MODE_CBC, iv)
print(cipher.decrypt(enc))