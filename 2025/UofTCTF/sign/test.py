XXPRIME_1 = 11400714785074694791
XXPRIME_2 = 14029467366897019727
XXPRIME_5 = 2870177450012600261

def XXROTATE(x):
    # rotate left 31 bits
    return ((x << 31) & 0xFFFFFFFFFFFFFFFF) | (x >> 33)

def tuplehash(t):
    acc = XXPRIME_5
    for x in t:
        lane = hash(x)
        acc += lane * XXPRIME_2
        acc &= 0xFFFFFFFFFFFFFFFF
        acc = XXROTATE(acc)
        acc *= XXPRIME_1
        acc &= 0xFFFFFFFFFFFFFFFF
    
    acc += len(t) ^ (XXPRIME_5 ^ 3527539)
    acc &= 0xFFFFFFFFFFFFFFFF
    return acc

def partialhash(t):
    acc = XXPRIME_5
    for x in t:
        lane = hash(x)
        acc += lane * XXPRIME_2
        acc &= 0xFFFFFFFFFFFFFFFF
        acc = XXROTATE(acc)
        acc *= XXPRIME_1
        acc &= 0xFFFFFFFFFFFFFFFF
        
    return acc

# print(tuplehash((1,2,3)))
# print(hash((1,2,3)))

from z3 import *
set_param("parallel.enable", True)
def XXROTATE_sym(x):
    return RotateLeft(x, 31)

def tuplehash_sym(t):
    acc = XXPRIME_5
    for x in t:
        lane = x # assume integral
        acc += lane * XXPRIME_2
        acc = acc 
        acc = XXROTATE_sym(acc)
        acc *= XXPRIME_1
        acc = acc 
    
    acc += len(t) ^ (XXPRIME_5 ^ 3527539)
    return acc

def partialhash_sym(t):
    acc = XXPRIME_5
    for x in t:
        lane = x # assume integral
        acc += lane * XXPRIME_2
        acc = XXROTATE_sym(acc)
        acc *= XXPRIME_1
        
    return acc

ADMIN = b'adminTokenPlsNoSteal'
hsh = hash(tuple(ADMIN))
print(hsh)


# for i in range(256):
    # print(i, tuplehash(bytes([i])), hash(tuple([i])) & 0xFFFFFFFFFFFFFFFF)



n = len(ADMIN)
msg = [BitVec(f'msg_{i}', 64) for i in range(n + 1)]
s = Solver()

for i in range(n):
    s.add(0 <= msg[i], msg[i] < 255)

s.add(tuplehash_sym(msg) == tuplehash(ADMIN))

if s.check() == sat:
    m = s.model()
    print(bytes([m[msg[i]].as_long() for i in range(n)])
)
else:
    print("unsat")
    
# for l in range(len(ADMIN) - 5):
#     r = l + 5
#     n = r - l
#     hsh = partialhash(tuple(ADMIN[l:r]))
#     # print(hsh)
#     msg = [BitVec(f'msg_{i}', 64) for i in range(n)]
#     s = Solver()
#     s.set("timeout", 60000)
#     for i in range(n):
#         s.add(0 <= msg[i], msg[i] < 255)
#         # s.add(msg[i] == ADMIN[i])

#     s.add(msg[0] != ADMIN[l])
#     s.add(partialhash_sym(msg) == hsh)

#     if s.check() == sat:
#         m = s.model()
#         print(l, r, bytes([m[msg[i]].as_long() for i in range(n)]))
#     else:
#         # print("unsat")
#         pass

# s.check()
# print(s.model().eval(partialhash_sym(msg)))