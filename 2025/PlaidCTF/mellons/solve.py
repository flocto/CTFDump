from chall import *
# from z3 import *
from cvc5.pythonic import *
from os import urandom
from functools import reduce
from tqdm import trange
import time
# set_param('parallel.enable', True)

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

ct = open('ct0.bin', 'rb').read()
# ct = open('ct1.bin', 'rb').read()
ct = split_nibbles(list(ct))
ct_blocks = [ct[i:i+16] for i in range(0, len(ct), 16)]
iv, *ct_blocks = ct_blocks

def symbolic_gs(x):
    bits = [Extract(i, i, x) for i in range(4)]
    return (bits[3] & bits[2]) ^ bits[2] ^ bits[1] ^ bits[0]

def symbolic_g(x):
    gx = reduce(lambda a, b: a ^ b, [symbolic_gs(nibble) for nibble in x])
    return simplify(gx)

def symbolic_split_nibbles(message_bytes):
    output = []
    for b in message_bytes:
        # extract the top 4 bits
        top = Extract(7, 4, b)
        # extract the bottom 4 bits
        bot = Extract(3, 0, b)
        output.append(top)
        output.append(bot)
    return output

def symbolic_unsplit_nibbles(message_bytes):
    output = []
    for i in range(0, len(message_bytes), 2):
        # combine the two nibbles
        combined = Concat(Extract(3, 0, message_bytes[i]), Extract(3, 0, message_bytes[i + 1]))
        output.append(combined)
    return output

def symbolic_compress(message_bytes):
    output = []
    prev = None # remainder from previous byte
    prev_size = 0
    for b in message_bytes:
        if prev_size == 0:
            # extract the bottom 7 bits
            prev = Extract(6, 0, b)
            prev_size = 7
        else:
            rem = 8 - prev_size
            # append top rem bits of b
            output.append(Concat(prev, Extract(6, 6 - rem + 1, b)))
            # remaining bits go to prev
            prev_size = 6 - rem + 1
            if prev_size != 0:
                # extract the remaining bits
                prev = Extract(6 - rem, 0, b)
    
    if prev_size != 0:
        # pad with 0s
        prev = Concat(prev, BitVecVal(0, 8 - prev_size))
        output.append(prev)

    return output
        
def symbolic_decompress(message_bytes):
    output = []
    prev = None # remainder from previous byte
    prev_size = 0

    for b in message_bytes:
        if prev_size == 0:
            # first 7 bits, pad to 8 bits
            top = Extract(7, 1, b)
            output.append(ZeroExt(1, top))
            prev = Extract(0, 0, b)
            prev_size = 1
        else:
            rem = 7 - prev_size
            # append top rem bits of b
            top = Concat(prev, Extract(7, 7 - rem + 1, b))
            # pad to 8 bits
            output.append(ZeroExt(1, top))
            # remaining bits go to prev
            prev_size = 7 - rem + 1
            if prev_size != 0:
                # extract the remaining bits
                prev = Extract(7 - rem, 0, b)

            # edge case
            if prev_size == 7:
                # we simply take the rest as a new byte
                rest = Extract(6, 0, b)
                output.append(ZeroExt(1, rest))
                prev = None
                prev_size = 0
    
    # we dont need to worry about the last overflow
    # since it will be padding
    return output

def bytes2symvec(byts):
    return [BitVecVal(b, 8) for b in byts]

s = Solver()
flag_inner = [BitVec(f'flag_{i}', 8) for i in range(41)]
flag = bytes2symvec(b'PCTF{') + flag_inner + bytes2symvec(b'}')
message = bytes2symvec(b'PPPMSG:PPPMSG:') + flag * 3000
# message = bytes2symvec(b'P' * 7000)
# c = BitVec('c', 8)
# message = [c] * 7000

# ascii
s.add([And(b >= 0x20, b <= 0x7e) for b in flag])

pt = symbolic_compress(message)
padding_needed = 8 - (len(pt) % 8)
padding = bytes2symvec([padding_needed] * padding_needed)
pt = symbolic_split_nibbles(list(pt) + padding)
pt_blocks = [pt[i:i+16] for i in range(0, len(pt), 16)]
print(len(pt_blocks), len(ct_blocks))

for i in trange(len(pt_blocks)):
    pt_block = pt_blocks[i]
    pt_block = [a ^ b for (a,b) in zip(pt_block, iv)]
    ct_block = ct_blocks[i]
    
    gp = symbolic_g(pt_block)
    gc = g(ct_block)
    s.add(gp == gc)

    iv = ct_block

print("solving...")
start = time.time()
if s.check() == sat:
    m = s.model()
    print("SAT")
    print("Time:", time.time() - start)
    while s.check() == sat:
        m = s.model()
        inner_flag_bytes = [m.eval(flag_inner[i]).as_long() for i in range(len(flag_inner))]
        inner_flag = bytes(inner_flag_bytes)
        print("PCTF{" + inner_flag.decode() + "}")
        s.add(Or([flag_inner[i] != inner_flag_bytes[i] for i in range(len(flag_inner))]))

else:
    print("UNSAT")