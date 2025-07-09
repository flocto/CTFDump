import array

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

i = 0
disas = []
flag_idx = 0
while i < len(insts):
    inst = insts[i]
    if inst not in ops:
        disas.append(f'Unknown instruction {inst} at index {i}')
        i += 1
        continue

    op, size = ops[inst]
    args = insts[i + 1:i + 1 + size]
    op_str = f'{i:05x} | '
    match inst:
        case 0:
            op_str += f'r{args[0]} = 0'
        case 1:
            op_str += f'r{args[0]} = 1'
        case 2:
            op_str += f'r{args[0]} += {args[1]}'
        case 3:
            op_str += f'r{args[0]} -= {args[1]}'
        case 4:
            op_str += f'r{args[0]} <<= {args[1]}'
        case 5:
            op_str += f'r{args[0]} += r{args[1]}'
        case 6:
            op_str += f'r{args[0]} -= r{args[1]}'
        case 7:
            op_str += f'r{args[0]} ^= r{args[1]}'
        case 8:
            offset = args[1]
            addr = i + 3 + offset
            addr &= 0xfffff
            op_str += f'mem[{addr:05x}] = r{args[0]}'
        case 9:
            offset = args[1]
            addr = i + 3 + offset
            addr &= 0xfffff
            op_str += f'r{args[0]} = mem[{addr:05x}]'
        case 0xa:
            offset = args[0]
            addr = i + offset
            addr &= 0xfffff
            op_str += f'JE  {addr:05x}'
        case 0xb:
            offset = args[0]
            addr = i + offset
            addr &= 0xfffff
            op_str += f'JNE {addr:05x}'
        case 0xc:
            offset = args[0]
            addr = i + offset
            addr &= 0xfffff
            op_str += f'JMP {addr:05x}'
        case 0xd:
            op_str += f'r35 = FLAG[{flag_idx}]'
            flag_idx += 1
        case 0xe:
            # print(i + args[0], insts[i + args[0]])
            s, _ = parse_str(i + args[0] + 2)
            op_str += f'print "{s}"'
        case 0xf:
            op_str += 'exit'

    disas.append(f'{op_str}')
    i += 1 + size
    
    if inst == 0xf:
        break

with open('disas.txt', 'w') as f:
    for line in disas:
        f.write(line + '\n')
