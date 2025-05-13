from chall import *
from os import urandom
from functools import reduce


def nibble2bits(nibble):
    bits = []
    for i in range(4):
        bits.append((nibble >> i) & 1)
    return bits
def bits2nibble(bits):
    nibble = 0
    for i in range(4):
        nibble |= (bits[i] << i)
    return nibble

# Then, the following gS : F42 → F is nonlinear invariant for S;
# gS(x) = (x[3] ∧ x[2]) ⊕ x[2] ⊕ x[1] ⊕ x[0].
def gs(x):
    x = nibble2bits(x)
    return (x[3] & x[2]) ^ x[2] ^ x[1] ^ x[0]

# g(x) = M15j=0 gS(si)
def g(x):
    return reduce(lambda a, b: a ^ b, [gs(nibble) for nibble in x])

message = compress(b'P' * 7000)
padding_needed = 8 - (len(message) % 8)
message = split_nibbles(list(message) + padding_needed * [padding_needed])

ct = open('ct1.bin', 'rb').read()
ct = split_nibbles(list(ct))

pt_blocks = [message[i:i+16] for i in range(0, len(message), 16)]
ct_blocks = [ct[i:i+16] for i in range(0, len(ct), 16)]
iv = ct_blocks[0]
ct_blocks = ct_blocks[1:]
print(len(pt_blocks), len(ct_blocks))

for i in range(len(pt_blocks)):
    pt_block = pt_blocks[i]
    pt_block = [a ^ b for (a,b) in zip(pt_block, iv)]
    ct_block = ct_blocks[i]
    
    gp = g(pt_block)
    gc = g(ct_block)
    if gp != gc:
        print(i, gp, gc)
        # print("gp", pt_block)
        # print("gc", ct_block)

    iv = ct_block

# test against real data
print("REAL KEY")
key = urandom(16)
message = compress(b'P' * 7000)
ct = encrypt(key, message)

padding_needed = 8 - (len(message) % 8)
message = split_nibbles(list(message) + padding_needed * [padding_needed])
ct = split_nibbles(list(ct))
pt_blocks = [message[i:i+16] for i in range(0, len(message), 16)]
ct_blocks = [ct[i:i+16] for i in range(0, len(ct), 16)]
iv = ct_blocks[0]
ct_blocks = ct_blocks[1:]
print(len(pt_blocks), len(ct_blocks))

err = 0
for i in range(len(pt_blocks)):
    pt_block = pt_blocks[i]
    pt_block = [a ^ b for (a,b) in zip(pt_block, iv)]
    ct_block = ct_blocks[i]
    
    gp = g(pt_block)
    gc = g(ct_block)
    if gp != gc:
        # print(i, gp, gc)
        # print("gp", pt_block)
        # print("gc", ct_block)
        err += 1

    iv = ct_block

print("err", err)