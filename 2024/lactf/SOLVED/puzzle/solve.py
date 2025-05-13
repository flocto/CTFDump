from Crypto.Util.strxor import strxor
from Crypto.Util.number import long_to_bytes, bytes_to_long

data = [
	0x08, 0x6b, 0xd0, 0xfe, 0x49, 0xcb, 0xac, 0x9b, 0x9c, 0xf7, 0x65, 0xba, 0x4b, 0xae, 0x95, 0x69,
	0x08, 0xf3, 0xbc, 0x4e, 0xed, 0x18, 0x4a, 0x6b, 0xe0, 0xde, 0xf4, 0x42, 0xe5, 0xd3, 0xd9, 0xa8,
	0xde, 0xf4, 0x42, 0xe5, 0xd3, 0xd9, 0xa8, 0x3c, 0xcf, 0x4a, 0x49, 0x71, 0x0e, 0x16, 0x16, 0x0a
]

data = bytearray(data)

buf = b'\x00' * 41
buf = bytearray(buf)

buf[0:16] = data[0:16]
buf[16:32] = data[16:32]
buf[25:41] = data[32:48]

data = '''5 7 4 6 3 1 9 2 8
9 6 8 4 5 2 1 7 3
1 2 3 8 9 7 5 6 4
3 4 1 7 8 5 6 9 2
7 9 6 2 4 3 8 5 1
8 5 2 9 1 6 4 3 7
2 8 9 3 6 4 7 1 5
6 3 5 1 7 8 2 4 9
4 1 7 5 2 9 3 8 6'''
data = [[int(x) for x in row.split()] for row in data.split('\n')]
data = sum(data, [])

buf2 = [0 for _ in range(41)]
for i in range(len(data)):
    buf2[i // 2] |= (data[i] - 1) << (4 * (i % 2))

buf2 = bytearray(buf2)

buf = strxor(buf, buf2)

data = bytes_to_long(buf[::-1])
msg = []

while data:
    msg.append((data & ((1 << 6) - 1)) + 64)
    data >>= 6

print(bytes(msg))