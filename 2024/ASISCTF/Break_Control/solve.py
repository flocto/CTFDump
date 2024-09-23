import struct
import ctypes

# libc = ctypes.CDLL('libc.so.6')
# seed = 0x0000000066ef83bd
# libc.srand(seed)

data = open('originalflag.enc', 'rb').read()

data, uniq_perm = data[:-624], data[-624:]

data = struct.unpack(f'<{len(data)//8}Q', data)
print(len(data))
# print(list(data).index(0x416019d4b6a7cd76, 290))

uniq_perm = struct.unpack('<312H', uniq_perm)
print(uniq_perm)

# block = [libc.rand() % 1248 for _ in range(5)]

# for i in range(936):
#     block = block[1:] + [libc.rand() % 1248]
#     if list(uniq_perm[:5]) == block:
#         print(i)
#         break

# for _ in range(312):
#     libc.rand()

base = 8554
start = 601
offset = 133

def unpack_tuple(x):
    return x >> 6, x & 0x3f

bits = []
for i in range(1248):
    idx, bit = unpack_tuple(base + i)
    b = (data[idx - offset + start] >> bit) & 1
    bits.append(b)

# seen = set()
# while len(seen) < 616:
#     idx = libc.rand() % 9802
#     if idx in seen: continue
#     seen.add(idx)
#     if idx > base:
#         # print(idx - base)
#         bits[idx - base] ^= 1

for p in uniq_perm[::-1]:
    bits = bits[:p] + bits[p+1:]
print(bits)

dat = b''.join([int(''.join(map(str, bits[i:i+8])), 2).to_bytes(1, 'big') for i in range(0, len(bits), 8)])
print(dat)