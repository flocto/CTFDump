# from z3 import *
from cvc5.pythonic import *
import time
import struct

SIZE = 16 * 8
MASK = (1 << SIZE) - 1

def vpclmulqdq(a, b, imm=0):
    """
    Implement the PCLMULQDQ instruction.
    
    Args:
        a: First XMM register (128-bit integer)
        b: Second XMM register (128-bit integer)
        imm: Immediate value determining which 64-bit halves to multiply
             0: low half of a * low half of b
             1: high half of a * low half of b
             16: low half of a * high half of b
             17: high half of a * high half of b
    
    Returns:
        128-bit integer result
    """
    # Extract the 64-bit halves based on imm
    a_low = a & 0xFFFFFFFFFFFFFFFF
    a_high = a >> 64
    b_low = b & 0xFFFFFFFFFFFFFFFF
    b_high = b >> 64
    
    # Select operands based on imm
    if imm == 0:
        operand1, operand2 = a_low, b_low
    elif imm == 1:
        operand1, operand2 = a_high, b_low
    elif imm == 16:
        operand1, operand2 = a_low, b_high
    elif imm == 17:
        operand1, operand2 = a_high, b_high
    else:
        raise ValueError("Invalid immediate value for pclmulqdq")
    
    # Implement carry-less multiplication
    result = 0
    for i in range(64):
        if (operand2 >> i) & 1:
            result ^= operand1 << i
    
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


xmm0 = 0x73757379737375734242424232323232
pcl_res = vpclmulqdq(xmm0, xmm0, 0x10)
print(hex(pcl_res))

x = BitVec('x', SIZE)
x_low = Extract(63, 0, x)
x_high = Extract(127, 64, x)
pcl_res = sym_vpclmulqdq(x, x, 0x10)
target = 0x10245749e3ba11d32975cc235edbf76d
s = Solver()

s.add(pcl_res == target)
s.add(UGE(x, 0))

# word index 5
word_index = Extract(16 * 6 - 1, 16 * 6 - 16, x)
s.add(word_index == int.from_bytes(b'd3', 'little'))

# lowest bit lol
s.add(Extract(0, 0, x_low) == 1)
s.add(Extract(0, 0, x_high) == 1)

start = time.time()
print("Solving...")
if s.check() == sat:
    m = s.model()
    x = m[x].as_long()
    print(f"Solution found: {hex(x)}")
    print(f"Verification: {vpclmulqdq(x, x, 0x10)}")
    print(f"Target:       {hex(target)}")
else:
    print("No solution found")
print(f"Time taken: {time.time() - start:.4f} seconds")