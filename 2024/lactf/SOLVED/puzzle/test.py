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

known = b'lactf{'

i = 0
for c in known:
    c = c - 64
    buf[i >> 3] ^= (c << (i & 7)) & 0xff
    if (i & 7) > 2:
        buf[(i >> 3) + 1] ^= (c >> (8 - (i & 7))) & 0xff
    i += 6

print(buf)

for i in range(10):
    n1, n2 = divmod(buf[i], 16)
    print(n2 + 1, n1 + 1)


# print(buf)

# for b in buf:
#     n1, n2 = divmod(b, 16)
#     print(bin(n1)[2:].zfill(4), bin(n2)[2:].zfill(4))


# data = b'\x01\x06\x03\x05\x04\x02\x0f\x00\x14\x02\x15\x07\x18\x04\x19\x05\x1c\x03\x20\x04\x21\x05\x22\x08\x26\x05\x2c\x00\x30\x08\x35\x06\x36\x01\x3b\x03\x47\x08\x4a\x06\x4b\x04\x4e\x02\x4f\x07'

# board = [[0 for _ in range(9)] for _ in range(9)]

# for i in range(0, len(data), 2):
#     idx, val = data[i:i+2]
#     r, c = divmod(idx, 9)
#     board[r][c] = val + 1

# print('\n'.join(' '.join(str(x) for x in row) for row in board))
