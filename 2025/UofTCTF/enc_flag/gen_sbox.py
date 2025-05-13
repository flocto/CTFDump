MOD = 2147483647
seed = 2033295305 
r = []
r.append(seed)

for i in range(1, 31):
    r.append((16807 * r[i-1]) % MOD)

print(r)

for i in range(31, 34):
    r.append(r[i-31])

for i in range(34, 344):
    r.append((r[i-31] + r[i-3]) & 0xFFFFFFFF)

def next_rand():
    global r
    x = (r[-31] + r[-3]) & 0xFFFFFFFF
    r.append(x)
    r = r[1:]
    return x >> 1

sbox = [-1] * 256

for b in range(0x40):
    idxs = next_rand() 
    for j in range(4):
        idx = idxs & 0xFF
        while sbox[idx & 0xFF] != -1:
            idx += 1
        sbox[idx & 0xFF] = 4 * b + j
        idxs >>= 8

print(sbox)

data = open('flag_old.enc', 'rb').read()
_sbox = list(data[:0x100])
print(_sbox)
print(_sbox == sbox)

for i in range(8):
    print(sbox.index(i), _sbox.index(i))

