import struct

def swapendian(x):
    return ((x << 24) & 0xff000000) | ((x << 8) & 0x00ff0000) | ((x >> 8) & 0x0000ff00) | ((x >> 24) & 0x000000ff)

def prng_successor(x, n):
    x = swapendian(x)
    for _ in range(n):
        x = (x >> 1) | ((x >> 16 ^ x >> 18 ^ x >> 19 ^ x >> 21) << 31)
        x &= 0xffffffff
    return swapendian(x)

def prng_predecessor(x, n):
    x = swapendian(x)
    for _ in range(n):
        x = (x << 1) & 0xffffffff | ((x << 15 ^ x << 17 ^ x << 18 ^ x << 20) & 0x80000000) >> 31
    return swapendian(x)

# print(prng_successor(prng_predecessor(11223344, 0x40), 0x40))

import z3
def swapendian_sym(x):
    return z3.Concat(z3.Extract(7, 0, x), z3.Extract(15, 8, x), z3.Extract(23, 16, x), z3.Extract(31, 24, x))

def prng_successor_sym(x, n):
    x = swapendian_sym(x)
    for _ in range(n):
        x = (z3.LShR(x, 1) | ((z3.LShR(x, 16) ^ z3.LShR(x, 18) ^ z3.LShR(x, 19) ^ z3.LShR(x, 21)) << 31)) & 0xffffffff
    return swapendian_sym(x)



state = b'\x86f\xf8{\x8dL\xaf\xee\x82!V\x80\xb3\xb9;\x0c_\x1f\x1a\xbf\xd2bB\x15'
state = struct.unpack('<' + 'I' * 6, state)
print(list(state))
print([hex(s) for s in state])
key = 0x11223344
state = [s ^ key for s in state]

print(hex(prng_successor(state[3], 0x40)))

s = z3.Solver()
x = z3.BitVec('x', 32)
s.add(prng_successor_sym(x, 0x40) == 0x7e7d47e2)

print(s.check())