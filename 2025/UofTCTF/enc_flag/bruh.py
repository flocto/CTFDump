from z3 import *
s = Solver()
def split_parts(n):
    return [Extract(i*8+7, i*8, n) for i in range(4)]

def join_parts(parts):
    return Concat(parts[3], parts[2], parts[1], parts[0])

original_state = [z3.BitVec('state_%d' % i, 32) for i in range(31)]
state = original_state.copy()
for i in range(31):
    s.add(original_state[i] < 2147483647)

for i in range(31, 34):
    state.append(state[i-31])

for i in range(34, 344):
    state.append((state[i-31] + state[i-3]))

for i in range(344, 1000):
    state.append((state[i-31] + state[i-3]))

r = [LShR(x, 1) for x in state[344:]]

data = open('flag_old.enc', 'rb').read()
sbox = list(data[:256])
inv_sbox = [sbox.index(i) for i in range(256)]
data = data[256:]

rands = []
for i in range(0, len(sbox), 4):
    idxs = inv_sbox[i] | (inv_sbox[i+1] << 8) | (inv_sbox[i+2] << 16) | (inv_sbox[i+3] << 24)
    print(i // 4, inv_sbox[i], inv_sbox[i+1], inv_sbox[i+2], inv_sbox[i+3])
    rands.append(idxs)

print(rands[:31])

s.add(rands[0] == r[0])
s.add(rands[1] == r[1])
s.add(rands[2] == r[2])
s.add(rands[3] - 1 == r[3])
s.add(rands[4] == r[4])


# s.add(original_state[1] == (16807 * original_state[0]) % 2147483647)
# test
# for i in range(31):
#     s.add(original_state[i] == x[i])
# s.add(original_state[0] == 1736587606)
# s.add(original_state[1] == 377647665)
# s.add(original_state[2] == 1310128770)

if s.check() == sat:
    m = s.model()
    original_state = [m[original_state[i]].as_long() for i in range(31)]
    print(original_state)
else:
    print('unsat')


