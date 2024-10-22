from parse import ops
from z3 import *

# stack = list(b'\x00' * 15 + b'A')
enc = open('output.bin', 'rb').read()

def solve_block(enc):
    base = [BitVec(f'base_{i}', 8) for i in range(16)]
    stack = base.copy()

    regs = [0] * 32
    for op, arg in ops:
        match op:
            case 'push_reg':
                stack.append(regs[arg - 1])
            case 'push_imm':
                stack.append(arg)
            case 'pop_reg':
                regs[arg - 1] = stack.pop(0)
            case 'add':
                a, b = stack.pop(0), stack.pop(0)
                if isinstance(a, int) and isinstance(b, int):
                    stack.append((a + b) & 0xff)
                else:
                    stack.append(a + b)
            case 'mul':
                a, b = stack.pop(0), stack.pop(0)
                if isinstance(a, int) and isinstance(b, int):
                    stack.append((a * b) & 0xff)
                else:
                    stack.append(a * b)
        
        # print(op, arg)
        # if op != 'add' and op != 'mul':
        # else:
        #     print(op)

    # print(regs, stack)
    # print(bytes(stack).hex())


    s = Solver()
    for i in range(16):
        s.add(stack[i] == BitVecVal(enc[i], 8))

    if s.check() == sat:
        m = s.model()
        print(''.join([chr(m[base[i]].as_long()) for i in range(16)]))
    else:
        print('unsat')
        
for i in range(0, len(enc), 16):
    solve_block(enc[i:i+16])