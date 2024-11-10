def rol8(n, r):
    return ((n << r) | (n >> (8 - r))) & 0xff

def ror8(n, r):
    return ((n >> r) | (n << (8 - r))) & 0xff


data = [0x59a0,0x4d6a,0x23de,0xc024,0xe264,0xb159,0x0772,0x5c7f]
data = b''.join([bytes([i >> 8, i & 0xff]) for i in data])

# A = 0x0003 << 16 | 0x43fd
A = 0x343fd
# B = 0x0026 << 16 | 0x9ec3
B = 0x269ec3
mod = 0x0001 << 0x1f
state = 0x1337

out = b''

for i in range(16):
    state = (A * state + B) % mod
    x = (state >> (8 * (i % 4))) & 0xff
    out += bytes([data[i] ^ x])

print(out)