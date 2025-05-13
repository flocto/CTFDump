from z3 import *
# from cvc5.pythonic import *
import time
import struct

SIZE = 16 * 8
MASK = (1 << SIZE) - 1

def vpclmulqdq(a, b, imm=0):
    """
    Implements the vpclmulqdq instruction in Python.
    a, b: 128-bit integers
    imm: Immediate value to select which 64-bit halves to multiply:
        0x00: a[63:0] * b[63:0]
        0x01: a[63:0] * b[127:64]
        0x10: a[127:64] * b[63:0]
        0x11: a[127:64] * b[127:64]
    Returns a 128-bit integer result of the carry-less multiplication.
    """
    a_low = a & 0xFFFFFFFFFFFFFFFF
    a_high = (a >> 64) & 0xFFFFFFFFFFFFFFFF
    b_low = b & 0xFFFFFFFFFFFFFFFF
    b_high = (b >> 64) & 0xFFFFFFFFFFFFFFFF
    
    if imm == 0x00:
        return clmul_64(a_low, b_low)
    elif imm == 0x01:
        return clmul_64(a_low, b_high)
    elif imm == 0x10:
        return clmul_64(a_high, b_low)
    elif imm == 0x11:
        return clmul_64(a_high, b_high)
    else:
        raise ValueError(f"Invalid immediate value: {imm}")

def clmul_64(a, b):
    """Carry-less multiplication of two 64-bit integers."""
    result = 0
    for i in range(64):
        if (b >> i) & 1:
            result ^= a << i
    return result & MASK

def sym_vpclmulqdq(a, b, imm=0):
    """
    Symbolic version of vpclmulqdq for Z3.
    a, b: BitVecs representing 128-bit integers
    imm: Immediate value to select which 64-bit halves to multiply
    Returns a BitVec representing the result of the carry-less multiplication.
    """
    a_low = Extract(63, 0, a)
    a_high = Extract(127, 64, a)
    b_low = Extract(63, 0, b)
    b_high = Extract(127, 64, b)
    a_low = ZeroExt(64, a_low)
    a_high = ZeroExt(64, a_high)
    b_low = ZeroExt(64, b_low)
    b_high = ZeroExt(64, b_high)

    if imm == 0x00:
        return clmul_64_sym(a_low, b_low)
    elif imm == 0x01:
        return clmul_64_sym(a_low, b_high)
    elif imm == 0x10:
        return clmul_64_sym(a_high, b_low)
    elif imm == 0x11:
        return clmul_64_sym(a_high, b_high)
    else:
        raise ValueError(f"Invalid immediate value: {imm}")
    
def clmul_64_sym(a, b):
    """Symbolic carry-less multiplication of two 64-bit BitVecs."""
    result = BitVecVal(0, SIZE)
    for i in range(64):
        result ^= (a << i) * ZeroExt(127, Extract(i, i, b))
    return simplify(result)

# Implements bv[idx] = b, where idx is concrete. Assumes 1 <= size
def updateBit(size, bv, idx, b):
    if idx == 0:
        return Concat(Extract(size-1, idx+1, bv), b)
    elif idx == size-1:
        return Concat(                            b, Extract(idx-1, 0, bv))
    else:
        return Concat(Extract(size-1, idx+1, bv), b, Extract(idx-1, 0, bv))

# Implements: bv[idx] = b, where idx can be symbolic. Assumes 1 <= size <= 2^8
def Update(size, bv, idx, b):
    for i in range(size):
        bv = If(BitVecVal(i, 8) == idx, updateBit(size, bv, i, b), bv)
    return bv

def sym_pext(src, mask, size=64):
    """
    Symbolic version of pext for Z3.
    Returns a BitVec representing the result of the parallel extract.
    """
    dest = BitVecVal(0, size)
    idx = BitVecVal(0, 8)

    for m in [Extract(i, i, mask) for i in range(size)]:
        # print(f"m: {m}")
        srcBit = Extract(0, 0, src)
        src    = LShR(src, 1)
        dest   = If(m == BitVecVal(1, 1), Update(size, dest, idx, srcBit), dest)
        idx    = If(m == BitVecVal(1, 1), idx+1, idx)

    # return simplify(dest)
    print('pext finished')
    return dest

def sym_vaddsubps(src1, src2):
    # Split 128-bit vectors into 4x 32-bit pieces
    src1_chunks = [Extract(i+31, i, src1) for i in range(0, 128, 32)]
    src2_chunks = [Extract(i+31, i, src2) for i in range(0, 128, 32)]

    result_chunks = []

    for idx, (a_bits, b_bits) in enumerate(zip(src1_chunks, src2_chunks)):
        # Treat 32 bits as IEEE754 float
        a_float = fpBVToFP(a_bits, Float32())
        b_float = fpBVToFP(b_bits, Float32())

        # Even index -> subtract, Odd index -> add
        if idx % 2 == 0:
            res_float = fpSub(RNE(), a_float, b_float)
        else:
            res_float = fpAdd(RNE(), a_float, b_float)

        # Pack float back into 32 bits
        res_bits = fpToIEEEBV(res_float)
        result_chunks.append(res_bits)

    # Concatenate chunks into 128 bits (high bits first!)
    result = Concat(*reversed(result_chunks))
    return result


# x = 0x31313131303030306767676766666666
# x = BitVecVal(x, SIZE)
# x_parts = [Extract(127, 96, x), Extract(95, 64, x), Extract(63, 32, x), Extract(31, 0, x)]
# x_rot = Concat(x_parts[0], x_parts[2], x_parts[3], x_parts[1])
# res = sym_vaddsubps(x, x_rot)
# res = simplify(res).as_long()
# print(hex(res))
# exit()

def vaddsubps(src1: int, src2: int) -> int:
    # Unpack 4 floats from each 128-bit int
    s1_0, s1_1, s1_2, s1_3 = struct.unpack('<4f', src1.to_bytes(16, 'little'))
    s2_0, s2_1, s2_2, s2_3 = struct.unpack('<4f', src2.to_bytes(16, 'little'))

    # Unrolled computation
    r0 = s1_0 - s2_0  # lane 0 (even) - subtract
    r1 = s1_1 + s2_1  # lane 1 (odd)  - add
    r2 = s1_2 - s2_2  # lane 2 (even) - subtract
    r3 = s1_3 + s2_3  # lane 3 (odd)  - add

    # Pack result
    result_bytes = struct.pack('<4f', r0, r1, r2, r3)
    result_int = int.from_bytes(result_bytes, 'little')
    return result_int


# x = 0x44444444434343434242424241414141
# x_low = x & 0xFFFFFFFFFFFFFFFF
# x_high = (x >> 64) & 0xFFFFFFFFFFFFFFFF

# x_low = BitVecVal(x_low, 64)
# x_high = BitVecVal(x_high, 64)

# pext = sym_pext(x_low, x_high).as_long()
# print(hex(pext))

# print(hex(vpclmulqdq(x, x, 0x10)))

first_16_sqr = 0x0e0e84cd0fbad07ba801dd1ab614e490
pext_res = 0x217fd7a7
# first_16_sqr = 0x11881188108a108a1181118110831083
# pext_res = 0x00000000000aab6d
k = BitVec('k', SIZE)
k_lo = k & 0xFFFFFFFFFFFFFFFF
k_hi = (k >> 64) & 0xFFFFFFFFFFFFFFFF
k_parts = [Extract(127, 96, k), Extract(95, 64, k), Extract(63, 32, k), Extract(31, 0, k)]
s = Solver()

# min_chr = b'!'[0]
# max_chr = b'~'[0]
# # known = b'AAAABBBBCCCC'
# for i in range(16):
#     k_chr = Extract(i * 8 + 7, i * 8, k)
#     s.add(k_chr >= min_chr)
#     s.add(k_chr <= max_chr)
#     # if i < len(known):
#     #     s.add(k_chr == known[i])

# print(hex(first_16_sqr))
# s.add(sym_vpclmulqdq(k, k, 0x10) == first_16_sqr)
# print(hex(pext_res))
# s.add(sym_pext(k_lo, k_hi) == BitVecVal(pext_res, 64))

k_rot = Concat(k_parts[0], k_parts[2], k_parts[3], k_parts[1])
s.add(sym_vaddsubps(k_rot, k) == 0x34c25f30675f2f906e5f33776e5f2ffa)
# s.add(k == 0x31313131303030306767676766666666)

print('start')
start = time.time()
while s.check() == sat:
    m = s.model()
    # test = m.eval(sym_vaddsubps(k, k_rot)).as_long()
    # print(hex(test))
    # print(test.to_bytes(SIZE // 8, 'little'))

    k_val = m[k].as_long()
    print(f"Found k: {k_val}")
    print(f"Found k: {k_val.to_bytes(SIZE // 8, 'little')}")
    s.add(k != k_val)

print("Done")
print('Time taken:', time.time() - start)
