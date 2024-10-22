dump = open('dump.txt', 'r').read().split()

mat = []
row = []
vec = []

i = 0
while i < len(dump):
    c = dump[i]
    if c.startswith('sx.d(') or c[1:].startswith('sx.d(') or c.startswith('zx.q(sx.d('):
        # print(dump[i : i + 3])
        row.append(dump[i: i + 3])
    if c == '==':
        vec.append(int(dump[i+1][:-1], 16))
        mat.append(row)
        row = []

    i += 1

mmat = []
for row in mat:
    idxs = set()
    coeffs = {}
    for r in row:
        inp = r[0].split('[', 1)[1].split(']')[0]
        idx = int(inp, 16)
        idxs.add(int(inp, 16))

        op = r[1]
        if op != '*':
            if op == '<<':
                print(r)
                coeff = int(r[2].replace(')', ''), 16)
                coeffs[idx] = 2 ** coeff
            else:
                print(r)
                coeffs[idx] = 1
        else:
            coeff = int(r[2].replace(')', ''), 16)
            coeffs[idx] = coeff
        
    for i in range(len(vec)):
        if i not in coeffs:
            print('missing', i)
            coeffs[i] = 0

    rrow = [coeffs[i] for i in range(len(vec))]
    mmat.append(rrow)

import numpy as np

m = np.array(mmat)
v = np.array(vec)



flag = np.linalg.solve(m, v)
print(flag)