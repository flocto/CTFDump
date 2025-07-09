import array
from z3 import *

elf = open('shadow_labyrinth', 'rb').read()

shuffle = elf[0x22c0:0x22c0+0x30]
checks = array.array('Q', elf[0x20e0:0x20e0+0xc*8])
nums = array.array('Q', elf[0x2140:0x2140+0xc*32])

s = Solver()
flag = [BitVec(f'flag_{i}', 8) for i in range(0x30)]
for c in flag:
    s.add(Or(
        And(c >= 0x41, c <= 0x5a),  # A-Z
        And(c >= 0x61, c <= 0x7a),  # a-z
        And(c >= 0x30, c <= 0x39),  # 0-9
        c == 0x5f,  # _
    ))

known = b'by_?dd?ng_?d_multiply1ng_w3_pl4y_4_l1?tl3_m3l0dy'
for i, c in enumerate(known):
    if c != b'?'[0]:
        s.add(flag[i] == c)

s_1 = [0] * len(flag)
for i in range(len(flag)):
    s_1[i] = flag[shuffle[i]]

for i, check in enumerate(checks):
    sum = 0
    for j in range(4):
        sum += ZeroExt(56, s_1[i*4 + j]) * nums[i*4 + j]
    s.add(sum == check)

if s.check() == sat:
    while s.check() == sat:
        m = s.model()
        print(''.join(chr(m[c].as_long()) for c in flag))
        s.add(Or([c != m[c] for c in flag]))
else:
    print('No solution found')