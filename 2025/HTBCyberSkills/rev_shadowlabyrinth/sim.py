import array
from collections import defaultdict
# from z3 import *
from cvc5.pythonic import *

insts = open('result.bin', 'rb').read()
insts = array.array('I', insts)

ops = {0: ('set reg 0', 1),
       1: ('set reg 1', 1),
       2: ('add const', 2),
       3: ('sub const', 2),
       4: ('shift const', 2),
       5: ('add reg', 2),
       6: ('sub reg', 2),
       7: ('xor reg', 2),
       8: ('set mem rel', 2),
       9: ('load reg rel', 2),
       0xa: ('jmp equal', 1),
       0xb: ('jmp not equal', 1),
       0xc: ('jmp', 1),
       0xd: ('load flag char', 0),
       0xe: ('printstr', 1),
       0xf: ('exit', 0), }

def parse_str(idx):
    """Parse a string from the instruction set."""
    s = ''
    while True:
        c = insts[idx]
        if c == 0:
            break
        s += chr(c)
        idx += 1
    return s, idx

flag = [BitVec(f'flag_{i}', 32) for i in range(35)]
s = Solver()
for i in range(35):
    s.add(flag[i] >= 0x20, flag[i] <= 0x7e) 
flag_idx = 0
# mem = {}
# regs = {}
mem = defaultdict(lambda: BitVecVal(0, 32))
regs = defaultdict(lambda: BitVecVal(0, 32))
i = 0
eq_flag = 0
JE_STATE = 0
FLAG_CHAR = None
PROD = 0
row = []
mat = []
vec = []
while i < len(insts):
    inst = insts[i]
    if inst not in ops:
        print(f'Unknown instruction {inst} at index {i}')
        break

    _, size = ops[inst]
    args = insts[i + 1:i + 1 + size]
    match inst:
        case 0:
            # op_str += f'r{args[0]} = 0'
            regs[args[0]] = BitVecVal(0, 32)
        case 1:
            # op_str += f'r{args[0]} = 1'
            regs[args[0]] = BitVecVal(1, 32)
        case 2:
            # op_str += f'r{args[0]} += {args[1]}'
            regs[args[0]] = regs[args[0]] + args[1]
            regs[args[0]] = simplify(regs[args[0]])
        case 3:
            # op_str += f'r{args[0]} -= {args[1]}'
            eq_flag = regs[args[0]] == args[1]
            eq_flag = simplify(eq_flag)
            regs[args[0]] = regs[args[0]] - args[1]
            regs[args[0]] = simplify(regs[args[0]])
        case 4:
            # op_str += f'r{args[0]} <<= {args[1]}'
            regs[args[0]] = regs[args[0]] << args[1]
            regs[args[0]] = simplify(regs[args[0]])
        case 5:
            # op_str += f'r{args[0]} += r{args[1]}'
            if JE_STATE == 1:
                # print(FLAG_CHAR, PROD)
                regs[args[0]] = FLAG_CHAR * PROD
            else:
                regs[args[0]] = regs[args[0]] + regs[args[1]]
                regs[args[0]] = simplify(regs[args[0]])
        case 6:
            # op_str += f'r{args[0]} -= r{args[1]}'
            eq_flag = regs[args[0]] == regs[args[1]]
            eq_flag = simplify(eq_flag)
            regs[args[0]] = regs[args[0]] - regs[args[1]]
            regs[args[0]] = simplify(regs[args[0]])
        case 7:
            # op_str += f'r{args[0]} ^= r{args[1]}'
            regs[args[0]] = regs[args[0]] ^ regs[args[1]]
            regs[args[0]] = simplify(regs[args[0]])
        case 8:
            offset = args[1]
            addr = i + 3 + offset
            addr &= 0xfffff
            # op_str += f'mem[{addr:05x}] = r{args[0]}'
            mem[addr] = regs[args[0]]
        case 9:
            offset = args[1]
            addr = i + 3 + offset
            addr &= 0xfffff
            # op_str += f'r{args[0]} = mem[{addr:05x}]'
            if 0x1ef7a <= addr <= 0x1ef9c:
                vec.append(mem[addr].as_long())
            regs[args[0]] = mem[addr]
        case 0xa:
            offset = args[0]
            addr = i + offset
            addr &= 0xfffff
            # op_str += f'JE  {addr:05x}'
            # if eq_flag == 0:
            # print(f'r36: {regs[36]}')
            # if input(f'{i:0x} JE {eq_flag} > ') == 'y':
            #     i = addr
            #     continue
            if JE_STATE == 0:
                JE_STATE = 1
                PROD = regs[36]
                FLAG_CHAR = simplify(regs[35] + 1)
                row.append(PROD.as_long())
                if len(row) == 35:
                    mat.append(row)
                    row = []
            elif JE_STATE == 1:
                i = addr
                JE_STATE = 0
                continue
        case 0xb:
            offset = args[0]
            addr = i + offset
            addr &= 0xfffff
            # op_str += f'JNE {addr:05x}'
            # input(f'{i:0x} JNE {eq_flag} > ')
            # if eq_flag != 0:
            #     i = addr
            #     continue
            # s.add(eq_flag == True)
        case 0xc:
            offset = args[0]
            addr = i + offset
            addr &= 0xfffff
            # op_str += f'JMP {addr:05x}'
            i = addr
            continue
        case 0xd:
            # op_str += f'r35 = FLAG[{flag_idx}]'
            regs[35] = flag[flag_idx]
            flag_idx += 1
        case 0xe:
            # print(i + args[0], insts[i + args[0]])
            pr, _ = parse_str(i + args[0] + 2)
            print(f'print "{pr}"')
        case 0xf:
            print('exit')
            break

    i += 1 + size
    
    if inst == 0xf:
        break


print(mat, vec)

from numpy.linalg import solve
from numpy import array

mat = array(mat, dtype='int32')
vec = array(vec, dtype='int32')

sol = solve(mat, vec)
print(bytes([round(x) for x in sol]))