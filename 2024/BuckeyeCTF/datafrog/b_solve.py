import z3

data = open('data', 'r').read().strip().split('\n')[18507:23507]

flag = [z3.BitVec(f'flag_{i}', 8) for i in range(24)]

def get_bit(idx):
    byt_idx, bit_idx = divmod(idx - 1, 8)
    return z3.Extract(bit_idx, bit_idx, flag[byt_idx])

def sign(x):
    if x == 0:
        return 0
    if x < 0:
        return -1
    return 1

s = z3.Solver()

for f in flag:
    s.add(f >= 32)
    s.add(f <= 126)

for line in data:
    if line.startswith('bc'):
        _, *idxs = line.split()
        idxs = list(map(int, idxs))
        
        eqs = []
        for idx in idxs:
            if sign(idx) == -1:
                eqs.append(get_bit(-idx) == 1)
            else:
                eqs.append(get_bit(idx) == 0)

        # all 3 cannot be true at the same time
        s.add(z3.Not(z3.And(*eqs)))

if s.check() == z3.sat:
    m = s.model()
    print(''.join(chr(m[flag[i]].as_long()) for i in range(24)))
else:
    print('unsat')
                