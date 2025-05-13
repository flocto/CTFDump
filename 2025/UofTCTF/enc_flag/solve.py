import aes
import struct

data = open('flag.enc', 'rb').read()
sbox = data[:0x100]
data = data[0x100:]
aes.s_box = sbox
inv_sbox = [sbox.index(i) for i in range(256)]
aes.inv_s_box = inv_sbox

MOD = 2147483647
seed = 2033295305 
# seed = 0x000000006782e940 
r = []
r.append(seed)

for i in range(1, 31):
    r.append((16807 * r[i-1]) % MOD)

print(r)

for i in range(31, 34):
    r.append(r[i-31])

for i in range(34, 344):
    r.append((r[i-31] + r[i-3]) & 0xFFFFFFFF)

for i in range(344, 1000):
    r.append((r[i-31] + r[i-3]) & 0xFFFFFFFF)

r = [x >> 1 for x in r[344:]]
print(r[0])
r = r[0x40:]
print([hex(x) for x in r[:10]])
key = struct.pack('<Q', r[0]) + struct.pack('<Q', r[1])
# key = struct.pack('<Q', 0x00000000201673d0) + struct.pack('<Q', 0x0000000032e0fede)
cipher = aes.AES(key)

dec = b''
for i in range(0, len(data), 16):
    print(i, data[i:i+16])
    dec += cipher.decrypt_block(data[i:i+16])
print(dec)
