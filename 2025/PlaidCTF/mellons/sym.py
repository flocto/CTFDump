from functools import reduce
from z3 import *
from chall import *

verification = compress(b'P' * 7000)
ct = open('ct1.bin', 'rb').read()

nibbles = split_nibbles(list(ct))

def bitcount(b):
    n = b.size()
    bits = [ Extract(i, i, b) for i in range(n) ]
    bvs  = [ Concat(BitVecVal(0, n - 1), b) for b in bits ]
    nb   = reduce(lambda a, b: a + b, bvs)
    return nb


key = [BitVec(f'key_{i}', 8) for i in range(16)]
# assert 32 < sum(k.bit_count() for k in key) <= 64
s = Solver()
s.add(32 < sum(bitcount(k) for k in key))
s.add(sum(bitcount(k) for k in key) <= 64)

key = split_nibbles(key)
K0 = key[:16]
K1 = key[16:32]
WK = [a ^ b for a,b in zip(K0, K1)]