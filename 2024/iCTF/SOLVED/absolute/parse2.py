# from z3 import *
# from cvc5.pythonic import *
import time

class FlagItem:
    def __init__(self, idx, coeffs, used=False):
        self.idx = idx
        self.coeffs = coeffs
        self.used = used

    def __mul__(self, other):
        # if not self.used:
        #     print('mul', self.idx, other, self.coeffs[self.idx], self.used)
        self.coeffs[self.idx] = other
        return FlagItem(self.idx, self.coeffs, True)
    
    def __lshift__(self, other):
        print('lshift', self.idx, other, self.coeffs[self.idx], self.used)
        if self.used:
            self.coeffs[self.idx] += self.coeffs[self.idx] << other
        else:
            self.coeffs[self.idx] = 1 << other
        return FlagItem(self.idx, self.coeffs, True)
    
    def __radd__(self, other):
        if not self.used:
            print('radd', self.idx, other, self.coeffs[self.idx], self.used)
        # self.coeffs[self.idx] = 1
        return FlagItem(self.idx, self.coeffs, True)
    
    
    def __add__(self, other):
        if not self.used:
            print('add', self.idx, other, self.coeffs[self.idx], self.used)
        # self.coeffs[self.idx] = 1
        return FlagItem(self.idx, self.coeffs, True)

class FlagBuf:
    def __init__(self):
        self.len = 0x2f
        self.coeffs = {i: 0 for i in range(self.len)}

    def __getitem__(self, idx):
        return FlagItem(idx, self.coeffs)
    
    def clear(self):
        self.coeffs = {i: 0 for i in range(self.len)}

dump = open('dump.txt', 'r').read().split('\n')
input = FlagBuf()

mat = []
vec = []

for line in dump[:-1]:
    try:
        line = line.split(None, 1)[1]
    except:
        continue
    if line.startswith('int32_t') or line.startswith('uint64_t'):
        line = line.split(None, 1)[1]
    line = line.replace('sx.d', '').replace('zx.q', '').replace('.d', '')

    if line.startswith('if'):
        expr = line.split('(', 1)[1].rsplit(')', 1)[0]
        lhs, rhs = expr.split('==')
        # print(lhs, rhs)
        lhs = eval(lhs)
        # print(input.coeffs)
        row = [0 for _ in range(0x2f)]
        for i in range(0x2f):
            row[i] = input.coeffs[i]
        mat.append(row)
        vec.append(int(rhs, 16))
        input.clear()
    else:
        # print(line)
        exec(line)

# print(mat, vec)

import numpy as np

mat = np.array(mat)
vec = np.array(vec)

f = np.linalg.solve(mat, vec)
print(f)
# print(mat @ f - vec)

print(''.join([chr(round(f[i])) for i in range(0x2f)]))