import struct
import ctypes
from tqdm import trange
from pwn import *
import time
libc = ctypes.CDLL('libc.so.6')
libc.srand(0x13371337)

# r = process(['./super_secure', 'hello'])
# nc challenge.ctf.uscybergames.com 60851
r = remote('challenge.ctf.uscybergames.com', 60851)

def rolq(x, n):
    return ((x << n) | (x >> (64 - n))) & 0xffffffffffffffff

main = (0x5ab ^ libc.time()) & 0xfff
print(hex(main))

data = open('super_secure', 'rb').read()

start = data[0x11e0:0x11e0 + 0x20000]
start = bytearray(start)
arr_offset = 0x6dd - 0x1e0

challenge = r.recvline_contains(b'challenge: ').decode().strip().split(': ', 1)[1].encode()
s = challenge
# for i in trange(0x100000):
#     seed = (i << 12) | main
#     libc.srand(seed)
    
#     first_4 = bytes([(libc.rand() % 94) + 0x20 for _ in range(4)])
#     if first_4 == s[:4]:
#         break

# print(hex(seed))
# libc.srand(seed)
# for i in range(64):
#     libc.rand()

libc.srand(0x13371337)
for i in range(0xffff):
    rc = libc.rand() & 0xffff
    start[arr_offset + i * 2:arr_offset + i * 2 + 2] = struct.pack('<H', rc)

res = 0
for i in range(0x40):
    res = rolq(res ^ s[i], 1)

# 0040139d        for (int32_t i = 0; i s<= 0xffff; i += 1)
# 0040132e            uint16_t tmp = i.w
# 0040132e            
# 00401383            for (int32_t j = 0; j s<= 2; j += 1)
# 00401353                int32_t idx = i + j
# 0040135a                uint32_t sign = idx s>> 0x1f u>> 0x1a
# 00401377                tmp = sx.w(s[sx.q(((idx + sign) & 0x3f) - sign)])
# 00401377                    + *(_start + zx.q(tmp) * 2)
# 00401377            
# 0040138d            result = rol.q(result ^ zx.q(tmp), 0x10)

for i in range(0x10000):
    tmp = i
    for j in range(3):
        idx = (i + j) % 64
        pt1 = s[idx]
        pt2 = int.from_bytes(start[tmp * 2:tmp * 2 + 2], 'little')
        # print(hex(pt1), hex(pt2))
        tmp = ctypes.c_uint16(pt1 + pt2).value
        # print(hex(tmp))
    
    res = rolq(res ^ tmp, 16)

print(res, hex(res))
# time.sleep(1.1) 
r.sendlineafter(b'>', str(res).encode())

for i in trange(99):
    challenge = r.recvline_contains(b'challenge: ').decode().split('challenge: ', 1)[1].encode()
    s = challenge

    # for i in range(64):
    #     libc.rand()

    # for i in range(0xffff):
    #     rc = libc.rand() & 0xffff
    #     start[arr_offset + i * 2:arr_offset + i * 2 + 2] = struct.pack('<H', rc)

    res = 0
    for i in range(0x40):
        res = rolq(res ^ s[i], 1)

    for i in range(0x10000):
        tmp = i
        for j in range(3):
            idx = (i + j) % 64
            sign = (idx >> 31) >> 26
            pt1 = s[(idx + sign) & 0x3f]
            pt2 = int.from_bytes(start[tmp * 2:tmp * 2 + 2], 'little')
            tmp = ctypes.c_uint16(pt1 + pt2).value
        
        res = rolq(res ^ tmp, 16)

    # print(res, hex(res))
    # time.sleep(1.1) 
    r.sendlineafter(b'>', str(res).encode())

r.interactive()