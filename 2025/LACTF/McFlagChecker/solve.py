import re

def op1(n):
    return (n * 97 + 129) % 256

def inv_op1(n):
    return (n - 126) * pow(97, -1, 256) % 256

mcfunc = open('data/chall/functions/check_flag.mcfunction').read()
reset = open('data/chall/functions/reset.mcfunction').read()

mat = [[0 for _ in range(40)] for _ in range(40)]
mat_reg = r"data merge block ([0-9]+) 0 ([0-9]+) .*Storage: ([0-9]+)"

for line in reset.split('\n'):
    m = re.match(mat_reg, line)
    if m:
        mat[int(m.group(1))][int(m.group(2))] = int(m.group(3))

out = [0] * 40
out_reg = r"execute unless score Global Reg([0-9]+) matches ([0-9]+)"

for line in mcfunc.split('\n'):
    m = re.match(out_reg, line)
    if m:
        out[int(m.group(1))] = int(m.group(2))

print(out)

pow_map = {}
for i in range(256):
    pow_map[pow(6, i, 251)] = i 

from sage.all import *
F = GF(251)
mat = matrix(F, mat)
out = vector(F, out)

out = mat.solve_right(out)
out = [pow_map[n] for n in out]
v1 = 106
for i in range(40):
    v1 = op1(v1)
    out[i] ^= v1
    

print(bytes(out))