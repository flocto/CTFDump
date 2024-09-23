import hashlib
from tqdm import trange

headers = [
    b'PK\x03\x04',
    b'PK\x05\x06',
    b'PK\x07\x08',
    b'\xff\xd8\xff\xe0',
    b'\xff\xd8\xff\xe1',
    b'\x89PNG',
]

# THANK YOU CHATGPT
def xxtea_encrypt(key: bytearray, v: bytearray, n: int) -> bytearray:
    z = v[n - 1]
    sum_value = (0x9E3779B9 * (52 // n) - 0x4AB325AA) & 0xFFFFFFFF
    rounds = 0
    delta = 0x61C88647

    while rounds != sum_value:
        rounds = (rounds - delta) & 0xFFFFFFFF
        e = (rounds >> 2) & 0xF

        # Main loop for all but the last element
        for p in range(n - 1):
            y = v[p + 1]
            v[p] = (v[p] + (((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4)) ^ ((rounds ^ y) + (key[(p ^ e) & 0xF] ^ z)))) & 0xFF
            z = v[p]

        # Process the last element (wrap-around)
        y = v[0]
        v[n - 1] = (v[n - 1] + (((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4)) ^ ((rounds ^ y) + (key[(n - 1 ^ e) & 0xF] ^ z)))) & 0xFF
        z = v[n - 1]

    return v

def xxtea_decrypt(key: bytearray, v: bytearray, n: int) -> bytearray:
    z = v[n - 1]
    y = v[0]
    sum_value = (0x9E3779B9 * (52 // n) - 0x4AB325AA) & 0xFFFFFFFF
    rounds = sum_value
    delta = 0x61C88647

    while rounds != 0:
        e = (rounds >> 2) & 0xF

        # Main loop for all but the first element
        for p in range(n - 1, 0, -1):
            z = v[p - 1]
            v[p] = (v[p] - (((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4)) ^ ((rounds ^ y) + (key[(p ^ e) & 0xF] ^ z)))) & 0xFF
            y = v[p]

        # Process the first element (wrap-around)
        z = v[n - 1]
        v[0] = (v[0] - (((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4)) ^ ((rounds ^ y) + (key[(0 ^ e) & 0xF] ^ z)))) & 0xFF
        y = v[0]

        rounds = (rounds + delta) & 0xFFFFFFFF

    return v


seen = set()
data = open('flag.enc', 'rb').read()[:-1]
print(len(data))
# print(data, len(data))
kettle = open('kettle', 'rb').read()
print(len(kettle))

# key = kettle[:16]
# for i in trange(15, len(kettle)):
#     key = key[1:] + bytes([kettle[i]])
#     key = hashlib.md5(key).digest()
#     if key in seen:
#         continue
#     seen.add(key)

#     enc = bytearray(data)
#     xxtea_decrypt(key, enc, len(enc))

#     if any(enc[:len(h)] == h for h in headers) or b'flag' in enc:
#         print(i, enc[:16], kettle[i:i+16])

i = 2921
key = kettle[i:i+16]
key = hashlib.md5(key).digest()
enc = bytearray(data)
xxtea_decrypt(key, enc, len(enc))

open('flag.png', 'wb').write(enc)
