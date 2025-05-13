from z3 import *
import struct

data = open('what', 'rb').read()

code = data[0x2008:0x2008 + 972]

solutions = data[0x3060:0x3060 + 8 * 0x3d]
solutions = [struct.unpack('<Q', solutions[i:i + 8])[0] for i in range(0, len(solutions), 8)]

s = Solver()
n = 0x3d
flag = [BitVec(f'flag_{i}', 8) for i in range(n)]
for i in range(0x3c):
    s.add(flag[i] >= 0x20)
    s.add(flag[i] <= 0x7e)


cur = None
i = 0
idx = 0
what = b'WHAT'
for c in code:
    if c == b'?'[0]:
        cur = ZeroExt(56, flag[i])
    elif c == b'W'[0]:
        cur ^= BitVecVal(what[idx % 4], 64)
        idx += 1
    elif c == b'H'[0]:
        cur += BitVecVal(what[idx % 4], 64)
        idx += 1
    elif c == b'A'[0]:
        cur *= BitVecVal(what[idx % 4], 64)
        idx += 1
    elif c == b'T'[0]:
        s.add(cur == BitVecVal(solutions[i], 64))
        i += 1
        cur = None
    else:
        break

if s.check() == sat:
    m = s.model()
    flag = [m[flag[i]].as_long() for i in range(n)]
    print(''.join([chr(i) for i in flag]))
else:
    print('No solution found')