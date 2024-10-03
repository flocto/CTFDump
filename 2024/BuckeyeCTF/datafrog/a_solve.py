import z3

data = open('data', 'r').read().strip().split('\n')[:18315]

groups = {}

for line in data:
    if line.startswith('ac'):
        _, x, i = line.split()
        x, i = int(x), int(i)
        if i not in groups:
            groups[i] = []
        groups[i].append(x)

flag = [z3.BitVec(f'flag_{i}', 8) for i in range(24)]

def get_bit(idx):
    byt_idx, bit_idx = divmod(idx, 8)
    return z3.Extract(bit_idx, bit_idx, flag[byt_idx])

s = z3.Solver()

for i in groups:
    eqs = []
    for g in groups[i]:
        idx = g >> 1
        val = 1 ^ (g & 1)

        eqs.append(get_bit(idx) == val)

    s.add(z3.Or(*eqs))

if s.check() == z3.sat:
    m = s.model()
    print(''.join(chr(m[flag[i]].as_long()) for i in range(24)))
else:
    print('unsat')
