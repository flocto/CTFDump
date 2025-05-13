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

ADMIN = b'adminTokenPlsNoSteal'

found = {}
for i in range(len(ADMIN) - 3):
    found[partialhash(ADMIN[i:i+4])] = ADMIN[i:i+4]

import itertools
for b in itertools.product(range(256), repeat=4):
    hsh = partialhash(bytes(b))
    if hsh in found:
        print(hsh, found[hsh], bytes(b))