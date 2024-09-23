import struct

XXTEA_DELTA = 0x9E3779B9


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

key = b'abcd1234ABCD1234'


data = b'hello this is sample messag\x01'

data = bytearray(data)
xxtea_encrypt(key, data, len(data))
print(data.hex())


data = open('out.enc', 'rb').read()[:-1]
print(data.hex(), len(data))
# # print(data, len(data))
# kettle = open('kettle', 'rb').read()

data = bytearray(data)

xxtea_decrypt(key, data, len(data))
print(data.hex(), data)

