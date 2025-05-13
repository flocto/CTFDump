from params import *
from sage.all import *
from secret_key import key
import random

F = GF(p)
key = vector(F, key)

idxs = list(random.choices(range(m), k=1024))
other_idxs = [i for i in range(m) if i not in idxs]

a = [[F(i) for i in ciphertexts[j]] for j in idxs]
M = Matrix(F, [i[:1024] for i in a])
v = vector(F, [i[-1] - (p//q) for i in a])

print(M.solve_right(v))

a = [[F(i) for i in ciphertexts[j]] for j in other_idxs]
M = Matrix(F, [i[:1024] for i in a])
v = vector(F, [i[-1] - (p//q) for i in a])

print(M.solve_right(v))