data = open('flag_old.enc', 'rb').read()
sbox = list(data[:256])
inv_sbox = [sbox.index(i) for i in range(256)]
data = data[256:]

def split_parts(n):
    return [(n >> (i*8)) & 0xFF for i in range(4)]

def join_parts(parts):
    return sum((parts[i] << (i*8)) for i in range(4))

rands = []
for i in range(0, len(sbox), 4):
    r = inv_sbox[i] | (inv_sbox[i+1] << 8) | (inv_sbox[i+2] << 16) | (inv_sbox[i+3] << 24)
    # print(i // 4, inv_sbox[i], inv_sbox[i+1], inv_sbox[i+2], inv_sbox[i+3])
    rands.append(r)

print(rands[:31])

def next_rand(r):
    return (((r[-31] << 1) + (r[-3] << 1) ) & 0xFFFFFFFF) >> 1

# print(rands[0], split_parts(rands[0]), [sbox[i] for i in split_parts(rands[0])])

# print(split_parts(rands[31]), split_parts(next_rand(rands[:31])))
state = rands[:31]
filled = set()

for i in range(31):
    parts = split_parts(rands[i])
    state_parts = []
    for p in parts:
        filled.add(p)
        while (t := p - 1) in filled:
            p -= 1
        state_parts.append(p)
    state[i] = join_parts(state_parts)


# print(filled)

# for i in range(31, len(rands)):
#     r = split_parts(rands[i])
#     nr = split_parts(next_rand(state))
#     print(r, nr, [ri in filled for ri in r], [nri in filled for nri in nr])
#     testr = join_parts([min(x, y) for x, y in zip(r, nr)])
#     print(testr, split_parts(testr))
#     filled.update(split_parts(testr))
#     state.append(testr)
#     state = state[1:]

MOD = 2147483647
seed = 1736587606
r = []
r.append(seed)

for i in range(1, 31):
    r.append((16807 * r[i-1]) % MOD)

for i in range(31, 34):
    r.append(r[i-31])

for i in range(34, 344):
    r.append((r[i-31] + r[i-3]) & 0xFFFFFFFF)

for i in range(344, 1000):
    r.append((r[i-31] + r[i-3]) & 0xFFFFFFFF)

r = [x >> 1 for x in r[344:]]
for i in range(31):
    if r[i] == state[i]:
        print(i, r[i], split_parts(r[i]), state[i], split_parts(state[i]))

