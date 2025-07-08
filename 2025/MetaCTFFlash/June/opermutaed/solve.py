from z3 import *
import struct
# You'll need to define the ints array based on the binary
# For now, I'll create a placeholder - you need to extract these values
# ints = [0] * 15  # Replace with actual values from the binary
ints = struct.unpack('<15I', b'\x0b`_?\x0eX\xf0c}Vm;\xd4b]%\"\x812\xc8\xa7E\x05k\xd8-\x05x\xcb\xe3\xf0\xe1\xbf\xd8\xe1\xb4\xd8\x13\xcf{\x0b C\x86\x99f\n\x9fV6M\x8d\xcb\xb7G\xec\":\xc1|')

def solve_flag():
    s = Solver()
    
    # Input is 43 characters
    flag = [BitVec(f'flag_{i}', 8) for i in range(43)]
    
    # Constrain to printable ASCII
    for i in range(43):
        s.add(flag[i] >= 32)
        s.add(flag[i] <= 126)
    
    # Process in groups of 3 from right to left
    group_count = 0
    pos = 42  # Start from the end (0-indexed)
    
    # FNV-1a hash initialization
    fnv_hash = BitVecVal(0xcbf29ce484222325, 64)
    
    while pos >= 0:
        # Get a, b, c (from right to left)
        if pos >= 0:
            a = flag[pos]
            pos -= 1
        else:
            a = BitVecVal(0, 8)
            
        if pos >= 0:
            b = flag[pos]
            pos -= 1
        else:
            b = BitVecVal(0, 8)
            
        if pos >= 0:
            c = flag[pos]
            pos -= 1
        else:
            c = BitVecVal(0, 8)
        
        # Calculate the transformation
        combined = ZeroExt(24, c) << 16 | ZeroExt(24, b) << 8 | ZeroExt(24, a)
        result = (combined * 0x5f356495) ^ 0xa6c3e1d2
        result_32 = Extract(31, 0, result)
        
        # Check against ints array (if we're within bounds)
        if group_count < 15:
            s.add(result_32 == ints[group_count])
        
        # Update FNV hash
        fnv_hash = fnv_hash ^ ZeroExt(32, result_32)
        fnv_hash = fnv_hash * 0x100000001b3
        
        group_count += 1
        
        # Break if we've processed enough groups
        if pos < 0:
            break
    
    # Final hash check
    s.add(fnv_hash == 0x1e53faf3038bff37)
    
    # Solve
    if s.check() == sat:
        model = s.model()
        flag_bytes = [model[flag[i]].as_long() for i in range(43)]
        flag_str = ''.join(chr(b) for b in flag_bytes)
        print(f"Flag: {flag_str}")
    else:
        print("No solution found")
    
if __name__ == "__main__":
    solve_flag()