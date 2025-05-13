from z3 import *

inp = b'aaaaggggAAAA0000bbbb1111CCCC2222'

res = []
for i in range(8):
    s = 0
    for j in range(4):
        s += inp[i + j]
    res.append(s)

print(res)

inp = [BitVecVal(x, 16) for x in inp]
min_chr = b'!'[0]
max_chr = 128

target = [526, 579, 588, 537, 484, 423, 426, 407]

s = Solver()

for i in range(8):
    x = 0
    for j in range(4):
        x += inp[i + j]
    s.add(x == target[i])

for i in range(32):
    s.add(UGE(inp[i], min_chr))
    s.add(ULE(inp[i], max_chr))

print(s.check())

