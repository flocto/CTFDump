# from z3 import *
from cvc5.pythonic import *

def mpsadbw(source1, source2, imm8=0):
    result = []

    source1 = source1.to_bytes(32, 'little')
    source2 = source2.to_bytes(32, 'little')
    # source2 = source2[::-1]

    BLK2_OFFSET = (imm8 & 0x3) * 4
    BLK1_OFFSET = ((imm8 >> 2) & 0x1) * 4

    # low bytes
    for i in range(8):
        s = 0
        for j in range(4):
            src1_byte = source1[i + j + BLK1_OFFSET]
            src2_byte = source2[j + BLK2_OFFSET]

            s += abs(src1_byte - src2_byte)
        result.append(s)
    
    # BLK2_OFFSET = ((imm8 >> 3) & 0x3) * 4
    # BLK1_OFFSET = ((imm8 >> 5) & 0x1) * 4
    # # high bytes
    # for i in range(8):
    #     s = 0
    #     for j in range(4):
    #         src1_byte = source1[i + j + 16 + BLK1_OFFSET]
    #         src2_byte = source2[j + 16 + BLK2_OFFSET]

    #         s += abs(src1_byte - src2_byte)
    #     result.append(s)

    return result

# Z3 version of mpsadbw_256 that works with symbolic variables
def z3_mpsadbw_256(source1, source2, imm8):
    """
    Z3 implementation of the MPSADBW instruction based on pseudocode
    
    Args:
        source1_bytes: List of 32 Z3 BitVec variables (8-bit each)
        source2: Second 256-bit integer (as an int)
        imm8: Immediate 8-bit value
    
    Returns:
        A list of sixteen 16-bit Z3 BitVec values
    """
    source2 = source2.to_bytes(32, 'little')
    # source2 = source2[::-1]

    if type(source1) == bytes:
        source1 = [BitVecVal(b, 8) for b in source1]
    
    result = []
    
    BLK2_OFFSET = (imm8 & 0x3) * 4
    BLK1_OFFSET = ((imm8 >> 2) & 0x1) * 4

    # low bytes
    for i in range(8):
        s = 0
        for j in range(4):
            src1_byte = source1[i + j + BLK1_OFFSET]
            src2_byte = source2[j + BLK2_OFFSET]

            src1_byte = ZeroExt(8, src1_byte)
            src2_byte = BitVecVal(src2_byte, 16)

            s += If(
                SGE(src1_byte, src2_byte),
                src1_byte - src2_byte,
                src2_byte - src1_byte
            )
        result.append(s)
    
    BLK2_OFFSET = ((imm8 >> 3) & 0x3) * 4
    BLK1_OFFSET = ((imm8 >> 5) & 0x1) * 4
    # high bytes
    for i in range(8):
        s = 0
        for j in range(4):
            src1_byte = source1[i + j + 16 + BLK1_OFFSET]
            src2_byte = source2[j + 16 + BLK2_OFFSET]

            src1_byte = ZeroExt(8, src1_byte)
            src2_byte = BitVecVal(src2_byte, 16)

            s += If(
                SGE(src1_byte, src2_byte),
                src1_byte - src2_byte,
                src2_byte - src1_byte
            )
        result.append(s)

    return result
    

def solve_for_target():

    s = Solver()
    
    # Define 32 symbolic bytes for input
    inp_bytes = [BitVec(f'byte_{i}', 8) for i in range(32)]

    min_chr = b'!'[0]
    max_chr = b'~'[0]
    for i in range(32):
        s.add(UGE(inp_bytes[i], min_chr))
        s.add(ULE(inp_bytes[i], max_chr))
        # A-Za-z0-9_
        # s.add(Or(
        #     And(UGE(inp_bytes[i], ord('A')), ULE(inp_bytes[i], ord('Z'))),
        #     And(UGE(inp_bytes[i], ord('a')), ULE(inp_bytes[i], ord('z'))),
        #     And(UGE(inp_bytes[i], ord('0')), ULE(inp_bytes[i], ord('9'))),
        #     inp_bytes[i] == ord('_')
        # ))


    # for i in range(32):
    #     s.add(UGE(inp_bytes[i], min_chr))

    known = b'c'
    for i in range(len(known)):
        s.add(inp_bytes[i] == known[i])
    
    # Constants
    K = 0x1337c0dedeadbeef
    TARGET = 0x019701aa01a701e40219024c0243020e
    TARGET_2 = 0x01470161011e012e0159015a015f0188
    
    # Get results as 16 16-bit values
    result_parts = z3_mpsadbw_256(inp_bytes, K, 0)
    
    # Split TARGET into 8 16-bit values (little-endian)
    target_parts = [(TARGET >> (i*16)) & 0xFFFF for i in range(8)]
    print([hex(part) for part in target_parts])

    # Add constraints for the lower 128 bits (8 values)
    for i in range(8):
        # print(f"result_parts[{i}]: {result_parts[i]}")
        s.add(result_parts[i] == target_parts[i])

    result_2_parts = z3_mpsadbw_256(inp_bytes, K, 5)

    target_2_parts = [(TARGET_2 >> (i*16)) & 0xFFFF for i in range(8)]
    print([hex(part) for part in target_2_parts])
    
    for i in range(8):
        # print(f"result_parts[{i}]: {result_2_parts[i]}")
        s.add(result_2_parts[i] == target_2_parts[i])

    if s.check() == sat:
        m = s.model()
        solution = [m[inp_bytes[i]].as_long() for i in range(32)]
        solution_bytes = bytes(solution)
        
        # Convert to int for verification
        solution_int = int.from_bytes(solution_bytes, 'little')
        
        # Verify the solution
        verification = mpsadbw(solution_int, K, 0) 
        
        print(f"Solution found: {solution_bytes.decode('ascii', errors='replace')}")
        print(f"Solution hex: {solution_bytes.hex()}")
        print(f"Verification: {verification[:8]}")
        print(f"Target:       {target_parts[:8]}")

        # while s.check() == sat:
        #     m = s.model()
        #     solution = [m[inp_bytes[i]].as_long() for i in range(32)]
        #     solution_bytes = bytes(solution)
        #     print(f"Another solution: {solution_bytes.decode('ascii', errors='replace')}")
        #     print(f"Another solution hex: {solution_bytes.hex()}")
        #     s.add(Or([inp_bytes[i] != solution_bytes[i] for i in range(32)]))
        
        return solution_bytes
    else:
        print("No solution found")
        return None

inp_bytes = b'aaaaggggAAAA0000bbbb1111CCCC2222'
# inp_bytes = bytes.fromhex('636b7cc49874498f5b7736212121212121212121212121212121212121212121')
inp = int.from_bytes(inp_bytes, 'little')

# inp_bytes = inp_bytes.ljust(32, b'\x00')
# print(inp_bytes)
# inp = int.from_bytes(inp_bytes, 'little')

# inp = 0x3232323243434343313131316262626230303030414141416767676746464646
# inp_bytes = inp.to_bytes(32, 'little')
# print(inp_bytes)
K =   0x1337c0dedeadbeef

IMM8 = 0
SIZE = 128
MASK = (1 << SIZE) - 1
result = mpsadbw(inp, K, IMM8) 
print(result)
print(f"{[hex(part) for part in result]}")

sym_result = z3_mpsadbw_256(inp_bytes, K, IMM8)
# for part in sym_result[:8]:
#     print(part)
print(f"{[simplify(part).as_long() for part in sym_result[:8]]}")
print(f"{[hex(simplify(part).as_long()) for part in sym_result[:8]]}")

# # Run the solver
# # if __name__ == "__main__":
# #     print("Solving for input that produces the target output...")
solution = solve_for_target()